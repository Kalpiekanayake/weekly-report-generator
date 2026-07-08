from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List


# Lightweight user summary embedded inside project responses
class ProjectMemberSummary(BaseModel):
    id: str
    full_name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ProjectOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    members: Optional[List[ProjectMemberSummary]] = []

    class Config:
        from_attributes = True
