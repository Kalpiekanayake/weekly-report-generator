from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.report import Report
from app.models.project import Project
from app.models.user import User
from app.schemas.report import ReportCreate, ReportUpdate, ReportOut, report_to_out

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/", response_model=ReportOut, status_code=status.HTTP_201_CREATED)
def create_report(
    report_in: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Validate project existence
    project = db.query(Project).filter(Project.id == report_in.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    # 2. Prevent duplicate reports for the same user and reporting week
    existing_report = db.query(Report).filter(
        Report.user_id == current_user.id,
        Report.week_start_date == report_in.week_start_date,
        Report.project_id == report_in.project_id
    ).first()
    
    if existing_report:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A report already exists for this project and week.",
        )

    # 3. Create report
    new_report = Report(
        user_id=current_user.id,
        **report_in.model_dump(),
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    # Need to load relationships for report_to_out to work correctly
    # Since we are in the same session, we can just access them after refresh.
    return report_to_out(new_report)


@router.get("/my/", response_model=List[ReportOut])
def get_my_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reports = db.query(Report).filter(Report.user_id == current_user.id).all()
    return [report_to_out(r) for r in reports]


@router.get("/{report_id}/", response_model=ReportOut)
def get_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

    # Access control: Owner or Manager
    if report.user_id != current_user.id and current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this report.",
        )

    return report_to_out(report)


@router.put("/{report_id}/", response_model=ReportOut)
def update_my_report(
    report_id: str,
    report_in: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

    # Access control: Must be owner
    if report.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own reports.",
        )
    
    # Check if draft
    if report.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only draft reports can be updated.",
        )

    # Update fields
    update_data = report_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(report, key, value)
    
    db.commit()
    db.refresh(report)
    return report_to_out(report)
