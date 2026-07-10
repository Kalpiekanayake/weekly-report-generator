from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, String
from datetime import date, timedelta

from app.core.database import get_db
from app.dependencies import require_manager
from app.models.user import User
from app.models.project import Project
from app.models.report import Report
from app.schemas.dashboard import DashboardStats, ProjectSummary, RecentActivity, AnalyticsData, ChartDataPoint

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
    late_reports = 0 
    pending_reports = 0
    
    # New metrics
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    total_reports_this_week = db.query(func.count(Report.id)).filter(Report.week_start_date == start_of_week).scalar()
    
    # Compliance rate: submitted / total_users (if > 0)
    compliance_rate = (submitted_reports / total_users * 100) if total_users > 0 else 0.0
    
    # Open blockers
    open_blockers = db.query(func.count(Report.id)).filter(Report.blockers != "").scalar()

    # Project summary
    projects = db.query(Project).all()
    project_summaries = []
    for project in projects:
        num_members = len(project.members)
        num_reports = len(project.reports)
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
        total_reports_this_week=total_reports_this_week,
        compliance_rate=compliance_rate,
        open_blockers=open_blockers,
        project_summaries=project_summaries,
        recent_activity=recent_activity
    )

@router.get("/analytics/", response_model=AnalyticsData)
def get_dashboard_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager),
):
    # 1. Reports submitted per week
    reports_per_week = db.query(
        Report.week_start_date.cast(String).label("week"), 
        func.count(Report.id).label("count")
    ).group_by(Report.week_start_date).all()
    reports_per_week_data = [ChartDataPoint(name=str(r.week), value=r.count) for r in reports_per_week]

    # 2. Reports by project
    reports_by_project = db.query(
        Project.name.label("name"), 
        func.count(Report.id).label("count")
    ).join(Report).group_by(Project.name).all()
    reports_by_project_data = [ChartDataPoint(name=r.name, value=r.count) for r in reports_by_project]

    # 3. Reports by team member
    reports_by_member = db.query(
        User.full_name.label("name"), 
        func.count(Report.id).label("count")
    ).join(Report).group_by(User.full_name).all()
    reports_by_member_data = [ChartDataPoint(name=r.name, value=r.count) for r in reports_by_member]

    # 4. Status distribution
    status_dist = db.query(
        Report.status.label("name"), 
        func.count(Report.id).label("count")
    ).group_by(Report.status).all()
    status_dist_data = [ChartDataPoint(name=r.name, value=r.count) for r in status_dist]

    # 5. Open blockers count by project (assuming blockers field exists in Report)
    # The requirement is "open blockers count". Assuming non-empty blockers field means "open".
    blockers_by_project = db.query(
        Project.name.label("name"),
        func.count(Report.id).filter(Report.blockers != "").label("count")
    ).join(Report).group_by(Project.name).all()
    blockers_data = [ChartDataPoint(name=r.name, value=r.count) for r in blockers_by_project]

    return AnalyticsData(
        reports_per_week=reports_per_week_data,
        reports_by_project=reports_by_project_data,
        reports_by_member=reports_by_member_data,
        status_distribution=status_dist_data,
        open_blockers_by_project=blockers_data
    )
