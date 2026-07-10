from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.dependencies import require_manager
from app.models.ai_chat import AIChatHistory
from app.models.user import User
from app.models.project import Project
from app.models.report import Report
from app.schemas.ai_chat import AIChatRequest, AIChatHistoryOut
from datetime import datetime, date, timedelta

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

def get_report_summary(db: Session, prompt: str):
    prompt_lower = prompt.lower()
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    
    reports = db.query(Report).filter(Report.week_start_date == start_of_week).all()
    all_reports = db.query(Report).all()

    if "work on" in prompt_lower or "summarize" in prompt_lower:
        if not reports: return "No reports have been submitted for this week yet."
        tasks = [f"{r.user.full_name}: {r.tasks_completed}" for r in reports]
        return f"This week, the team has been working on: " + "; ".join(tasks)
    
    elif "blockers" in prompt_lower:
        blockers = db.query(Project.name, func.count(Report.id)).join(Report).filter(Report.blockers != "").group_by(Project.name).all()
        if not blockers: return "No major blockers reported this week."
        return "Projects with open blockers: " + ", ".join([f"{p}: {c}" for p, c in blockers])

    elif "submitted" in prompt_lower:
        submitted = [r.user.full_name for r in all_reports if r.status == "submitted"]
        if not submitted: return "No members have submitted reports yet."
        return "Members who have submitted reports: " + ", ".join(set(submitted))
        
    elif "pending" in prompt_lower:
        pending = [r.user.full_name for r in all_reports if r.status == "draft"]
        if not pending: return "All reports are submitted."
        return "Members with pending reports: " + ", ".join(set(pending))

    return "I can help summarize team activity, report blockers, or list submission status. Try asking 'What did the team work on this week?' or 'Which reports are still pending?'"

@router.post("/chat", response_model=AIChatHistoryOut)
def chat(
    payload: AIChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager),
):
    response_text = get_report_summary(db, payload.prompt)
    
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
