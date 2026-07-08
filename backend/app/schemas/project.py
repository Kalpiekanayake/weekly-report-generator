from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.user import UserOut

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class ProjectOut(ProjectBase):
    id: UUID
    created_at: datetime
    members: Optional[List[UserOut]] = []

    class Config:
        from_attributes = True
