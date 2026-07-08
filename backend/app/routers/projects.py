"""
routers/projects.py
--------------------
Project / category management endpoints.

Endpoint summary:
  POST   /api/v1/projects          → create project       (manager only)
  GET    /api/v1/projects          → list all projects     (any authenticated user)
  GET    /api/v1/projects/{id}     → get project by id     (any authenticated user)
  PUT    /api/v1/projects/{id}     → update project        (manager only)
  DELETE /api/v1/projects/{id}     → delete project        (manager only)

RBAC design:
  - Read operations (GET) use get_current_user — all authenticated roles may view projects
    so that Team Members can pick a project when submitting a weekly report.
  - Write operations (POST, PUT, DELETE) use require_manager — only managers may
    create, rename, or remove project categories.

Duplicate-name guard:
  - Project names must be unique (enforced at the DB level by the UNIQUE constraint
    and additionally checked here to return a clear 409 instead of a raw DB error).
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user, require_manager
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut

router = APIRouter(prefix="/projects", tags=["Projects"])


# ---------------------------------------------------------------------------
# POST /projects  — create a new project (manager only)
# ---------------------------------------------------------------------------
@router.post(
    "",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project / category",
    responses={
        409: {"description": "A project with this name already exists"},
    },
)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_manager),   # RBAC: managers only; user not needed in body
) -> ProjectOut:
    """
    Create a new project category.

    - Name must be unique (case-sensitive match against existing records).
    - Only users with the 'manager' role may call this endpoint.
    """
    # Duplicate-name guard — keeps the error message friendly instead of
    # exposing a raw IntegrityError from the database driver.
    existing = db.query(Project).filter(Project.name == payload.name.strip()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A project named '{payload.name}' already exists.",
        )

    project = Project(
        name=payload.name.strip(),
        description=payload.description.strip() if payload.description else None,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectOut.model_validate(project)


# ---------------------------------------------------------------------------
# GET /projects  — list all projects (any authenticated user)
# ---------------------------------------------------------------------------
@router.get(
    "",
    response_model=List[ProjectOut],
    status_code=status.HTTP_200_OK,
    summary="List all projects / categories",
)
def list_projects(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),   # RBAC: any authenticated role
) -> List[ProjectOut]:
    """
    Return all projects ordered alphabetically by name.

    Accessible by both Team Members (to select a project when filing a report)
    and Managers (for project management and filtering).
    """
    projects = db.query(Project).order_by(Project.name).all()
    return [ProjectOut.model_validate(p) for p in projects]


# ---------------------------------------------------------------------------
# GET /projects/{project_id}  — get single project (any authenticated user)
# ---------------------------------------------------------------------------
@router.get(
    "/{project_id}",
    response_model=ProjectOut,
    status_code=status.HTTP_200_OK,
    summary="Get a project by ID",
    responses={
        404: {"description": "Project not found"},
    },
)
def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),   # RBAC: any authenticated role
) -> ProjectOut:
    """
    Return the details of a single project, including its member list.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )
    return ProjectOut.model_validate(project)


# ---------------------------------------------------------------------------
# PUT /projects/{project_id}  — update a project (manager only)
# ---------------------------------------------------------------------------
@router.put(
    "/{project_id}",
    response_model=ProjectOut,
    status_code=status.HTTP_200_OK,
    summary="Update a project / category",
    responses={
        404: {"description": "Project not found"},
        409: {"description": "Another project already uses this name"},
    },
)
def update_project(
    project_id: str,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_manager),   # RBAC: managers only
) -> ProjectOut:
    """
    Update a project's name and/or description.

    - At least one field must be provided (Pydantic's Optional handles this;
      unchanged fields retain their current values).
    - If a new name is supplied, it is checked for uniqueness against other projects.
    - Only users with the 'manager' role may call this endpoint.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    # Name-uniqueness check — only run when the caller is actually changing the name
    if payload.name is not None:
        new_name = payload.name.strip()
        if new_name != project.name:
            conflict = (
                db.query(Project)
                .filter(Project.name == new_name, Project.id != project_id)
                .first()
            )
            if conflict:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"A project named '{new_name}' already exists.",
                )
        project.name = new_name

    if payload.description is not None:
        project.description = payload.description.strip() if payload.description else None

    db.commit()
    db.refresh(project)
    return ProjectOut.model_validate(project)


# ---------------------------------------------------------------------------
# DELETE /projects/{project_id}  — delete a project (manager only)
# ---------------------------------------------------------------------------
@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project / category",
    responses={
        404: {"description": "Project not found"},
        409: {"description": "Project cannot be deleted — reports are linked to it"},
    },
)
def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_manager),   # RBAC: managers only
) -> None:
    """
    Permanently delete a project.

    - Returns 404 if the project does not exist.
    - Returns 409 if reports are still linked to this project.
      The Report model uses ON DELETE RESTRICT on its project_id foreign key,
      which means deleting a project with linked reports would raise a DB error.
      We detect this early and surface a clean 409 instead.
    - Returns 204 No Content on success (no body).
    - Only users with the 'manager' role may call this endpoint.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    # Guard: check for linked reports before attempting deletion.
    # WHY: Report.project_id has ON DELETE RESTRICT, so the DB would reject
    # the delete anyway — but we catch it here to return a clean HTTP 409
    # with a descriptive message instead of a raw 500 IntegrityError.
    if project.reports:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Cannot delete this project because it has linked weekly reports. "
                "Re-assign or delete those reports first."
            ),
        )

    db.delete(project)
    db.commit()
    # 204 No Content — FastAPI expects None / no return value here
