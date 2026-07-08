from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional

# --- Dashboard Summary KPIs ---
class DashboardSummary(BaseModel):
    total_members: int
    submitted_this_week: int
    pending_this_week: int
    compliance_rate: float  # percentage 0-100
    open_blockers_count: int
    total_reports_all_time: int

# --- Submission Status per member ---
class MemberSubmissionStatus(BaseModel):
    user_id: UUID
    full_name: str
    email: str
    status: str  # 'submitted', 'pending', 'late'
    submitted_at: Optional[datetime] = None

# --- Tasks Trend point ---
class TasksTrendPoint(BaseModel):
    week_start_date: str  # ISO date string
    tasks_count: int
    report_count: int

# --- Workload distribution by project ---
class WorkloadPoint(BaseModel):
    project_name: str
    report_count: int
    hours_worked: float

# --- Activity feed item ---
class ActivityItem(BaseModel):
    event: str
    user_full_name: str
    project_name: str
    week_start_date: str
    timestamp: datetime
