"""
schemas/report.py
-----------------
Pydantic request and response models for the Weekly Reports module.

Design decisions:
  - All ID fields use `str` (not uuid.UUID) to match the SQLAlchemy String(36)
    column type. Using UUID would cause model_validate() to fail because SQLAlchemy
    returns plain strings, not uuid.UUID objects.
  - `ReportOut` includes denormalised `user_full_name` and `project_name` fields
    for frontend convenience. These are not ORM columns — they are populated
    explicitly by a helper function (`report_to_out`) in the router layer.
  - `ReportUpdate` makes every field Optional so callers can send partial payloads
    (PATCH semantics over PUT).
  - Status on creation defaults to 'draft'. Submission is a separate endpoint
    (Part 2) to give the lifecycle explicit, auditable transitions.
"""

from datetime import datetime, date
from typing import Optional, Literal
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class ReportCreate(BaseModel):
    """Payload for POST /reports."""
    project_id: str = Field(..., min_length=36, max_length=36)
    week_start_date: date
    tasks_completed: str = Field(..., min_length=1)
    tasks_planned: str = Field(..., min_length=1)
    blockers: str = Field(..., min_length=1)
    hours_worked: Optional[float] = Field(None, ge=0, le=168)
    notes: Optional[str] = Field(None, max_length=2000)
    # Status on creation: draft (default) or submitted immediately
    status: Literal["draft", "submitted"] = "draft"


class ReportUpdate(BaseModel):
    """
    Payload for PUT /reports/{id}.

    All fields are optional — only provided fields will be applied.
    Only allowed on reports whose status is 'draft'.
    """
    project_id: Optional[str] = Field(None, min_length=36, max_length=36)
    week_start_date: Optional[date] = None
    tasks_completed: Optional[str] = Field(None, min_length=1)
    tasks_planned: Optional[str] = Field(None, min_length=1)
    blockers: Optional[str] = Field(None, min_length=1)
    hours_worked: Optional[float] = Field(None, ge=0, le=168)
    notes: Optional[str] = Field(None, max_length=2000)


# ---------------------------------------------------------------------------
# Response schema
# ---------------------------------------------------------------------------

class ReportOut(BaseModel):
    """
    Full report representation returned to the client.

    `user_full_name` and `project_name` are denormalised from the ORM
    relationships at serialisation time — they are NOT ORM columns, so
    `from_attributes = True` alone is insufficient. Use `report_to_out()`
    (defined below) to build this object correctly.
    """
    id: str
    user_id: str
    project_id: str
    week_start_date: date
    tasks_completed: str
    tasks_planned: str
    blockers: str
    hours_worked: Optional[float] = None
    notes: Optional[str] = None
    status: str
    submitted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    # Denormalised convenience fields populated by report_to_out()
    user_full_name: Optional[str] = None
    project_name: Optional[str] = None

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Helper: ORM → ReportOut
# ---------------------------------------------------------------------------

def report_to_out(report) -> ReportOut:
    """
    Convert a Report ORM object to ReportOut, populating the denormalised
    user_full_name and project_name fields from the ORM relationships.

    WHY a helper instead of model_validate() alone: SQLAlchemy relationships
    (`report.user`, `report.project`) are lazy-loaded and not direct column
    attributes, so Pydantic's from_attributes cannot map them automatically
    into `user_full_name` / `project_name`. We resolve them explicitly here
    while the DB session is still open.
    """
    return ReportOut(
        id=str(report.id),
        user_id=str(report.user_id),
        project_id=str(report.project_id),
        week_start_date=report.week_start_date,
        tasks_completed=report.tasks_completed,
        tasks_planned=report.tasks_planned,
        blockers=report.blockers,
        hours_worked=report.hours_worked,
        notes=report.notes,
        status=report.status,
        submitted_at=report.submitted_at,
        created_at=report.created_at,
        updated_at=report.updated_at,
        user_full_name=report.user.full_name if report.user else None,
        project_name=report.project.name if report.project else None,
    )
