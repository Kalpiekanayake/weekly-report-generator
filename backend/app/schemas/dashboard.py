from pydantic import BaseModel
from typing import List

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
    project_summaries: List[ProjectSummary]
    recent_activity: List[RecentActivity]
