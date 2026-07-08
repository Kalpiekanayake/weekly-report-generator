from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class AIChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)

class AIChatHistoryOut(BaseModel):
    id: UUID
    prompt: str
    response: str
    created_at: datetime

    class Config:
        from_attributes = True
