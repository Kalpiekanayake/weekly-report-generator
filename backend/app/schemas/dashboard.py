from pydantic import BaseModel
from typing import List, Optional

class ProjectSummary(BaseModel):
    project_name: str
    num_members: int
    num_reports: int
    completion_percentage: float

class RecentActivity(BaseModel):
    report_id: str
    user_name: str
    project_name: str
    week_start_date: str
    submitted_at: str

class DashboardStats(BaseModel):
    total_users: int
    total_projects: int
    total_reports: int
    draft_reports: int
    submitted_reports: int
    late_reports: int
    pending_reports: int
    total_reports_this_week: int
    compliance_rate: float
    open_blockers: int
    project_summaries: List[ProjectSummary]
    recent_activity: List[RecentActivity]

# --- Analytics Schemas ---

class ChartDataPoint(BaseModel):
    name: str
    value: int

class AnalyticsData(BaseModel):
    reports_per_week: List[ChartDataPoint]
    reports_by_project: List[ChartDataPoint]
    reports_by_member: List[ChartDataPoint]
    status_distribution: List[ChartDataPoint]
    open_blockers_by_project: List[ChartDataPoint]
