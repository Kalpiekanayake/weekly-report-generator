from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.dependencies import require_manager
from app.models.user import User
from app.models.project import Project
from app.models.report import Report
from app.schemas.dashboard import DashboardStats, ProjectSummary, RecentActivity

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/", response_model=DashboardStats)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager),
):
    # Summary stats
    total_users = db.query(func.count(User.id)).scalar()
    total_projects = db.query(func.count(Project.id)).scalar()
    total_reports = db.query(func.count(Report.id)).scalar()
    
    draft_reports = db.query(func.count(Report.id)).filter(Report.status == "draft").scalar()
    submitted_reports = db.query(func.count(Report.id)).filter(Report.status == "submitted").scalar()
    # Assuming "late" and "pending" are mapped to status values if they exist, 
    # but based on models only draft/submitted exist. 
    # For now, return 0 for late/pending as no definition for them in models.
    late_reports = 0 
    pending_reports = 0

    # Project summary
    projects = db.query(Project).all()
    project_summaries = []
    for project in projects:
        num_members = len(project.members)
        num_reports = len(project.reports)
        # Placeholder for completion %
        completion_percentage = 0.0 
        project_summaries.append(ProjectSummary(
            project_name=project.name,
            num_members=num_members,
            num_reports=num_reports,
            completion_percentage=completion_percentage
        ))

    # Recent activity
    recent_reports = db.query(Report).filter(Report.status == "submitted").order_by(Report.submitted_at.desc()).limit(5).all()
    recent_activity = []
    for report in recent_reports:
        recent_activity.append(RecentActivity(
            report_id=report.id,
            user_name=report.user.full_name,
            project_name=report.project.name,
            week_start_date=str(report.week_start_date),
            submitted_at=str(report.submitted_at)
        ))

    return DashboardStats(
        total_users=total_users,
        total_projects=total_projects,
        total_reports=total_reports,
        draft_reports=draft_reports,
        submitted_reports=submitted_reports,
        late_reports=late_reports,
        pending_reports=pending_reports,
        project_summaries=project_summaries,
        recent_activity=recent_activity
    )
