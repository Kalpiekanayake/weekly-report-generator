# Schemas package — re-exports all Pydantic validation models
from app.schemas.user import UserRegister, UserLogin, UserOut, Token, LoginResponse
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from app.schemas.report import ReportCreate, ReportUpdate, ReportOut
from app.schemas.ai_chat import AIChatRequest, AIChatHistoryOut
from app.schemas.dashboard import (
    DashboardStats, ProjectSummary, RecentActivity,
    AnalyticsData, ChartDataPoint,
)

__all__ = [
    "UserRegister", "UserLogin", "UserOut", "Token", "LoginResponse",
    "ProjectCreate", "ProjectUpdate", "ProjectOut",
    "ReportCreate", "ReportUpdate", "ReportOut",
    "AIChatRequest", "AIChatHistoryOut",
    "DashboardStats", "ProjectSummary", "RecentActivity",
    "AnalyticsData", "ChartDataPoint",
]
