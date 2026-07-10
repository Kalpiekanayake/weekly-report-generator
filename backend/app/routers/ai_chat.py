from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import require_manager
from app.models.ai_chat import AIChatHistory
from app.models.user import User
from app.schemas.ai_chat import AIChatRequest, AIChatHistoryOut
from datetime import datetime

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

@router.post("/chat", response_model=AIChatHistoryOut)
def chat(
    payload: AIChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager),
):
    # Mock AI response - production implementation would call an LLM API here
    response_text = f"As an AI Assistant, I've analyzed the reports. I cannot access real data yet, but for your prompt '{payload.prompt}', here is a sample response."
    
    new_chat = AIChatHistory(
        user_id=current_user.id,
        prompt=payload.prompt,
        response=response_text
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat

@router.get("/history", response_model=list[AIChatHistoryOut])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager),
):
    return db.query(AIChatHistory).filter(AIChatHistory.user_id == current_user.id).order_by(AIChatHistory.created_at.desc()).all()
