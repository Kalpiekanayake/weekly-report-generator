from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional

class ReportBase(BaseModel):
    project_id: UUID
    week_start_date: date
    tasks_completed: str = Field(..., min_length=1)
    tasks_planned: str = Field(..., min_length=1)
    blockers: str = Field(..., min_length=1)
    hours_worked: Optional[float] = Field(None, ge=0, le=168)
    notes: Optional[str] = None

class ReportCreate(ReportBase):
    # status can be 'draft' or 'submitted' on creation
    status: str = Field(default="draft", pattern="^(draft|submitted)$")

class ReportUpdate(BaseModel):
    project_id: Optional[UUID] = None
    week_start_date: Optional[date] = None
    tasks_completed: Optional[str] = Field(None, min_length=1)
    tasks_planned: Optional[str] = Field(None, min_length=1)
    blockers: Optional[str] = Field(None, min_length=1)
    hours_worked: Optional[float] = Field(None, ge=0, le=168)
    notes: Optional[str] = None

class ReportOut(ReportBase):
    id: UUID
    user_id: UUID
    status: str
    submitted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    # Denormalized fields for convenience on the frontend
    user_full_name: Optional[str] = None
    project_name: Optional[str] = None

    class Config:
        from_attributes = True
