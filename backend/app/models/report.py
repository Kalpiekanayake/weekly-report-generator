import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Date, Float, Uuid, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(Uuid, ForeignKey("projects.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    # Start date of the week (typically a Monday)
    week_start_date = Column(Date, nullable=False, index=True)
    
    # Core report sections (required)
    tasks_completed = Column(String, nullable=False)
    tasks_planned = Column(String, nullable=False)
    blockers = Column(String, nullable=False)
    
    # Optional sections
    hours_worked = Column(Float, nullable=True)
    notes = Column(String, nullable=True)
    
    # Lifecycle state: 'draft' or 'submitted'
    status = Column(String(50), default="draft", nullable=False)
    
    submitted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="reports")
    project = relationship("Project", back_populates="reports")

    # Enforce uniqueness of one report per project per week per user
    __table_args__ = (
        UniqueConstraint('user_id', 'week_start_date', 'project_id', name='uq_user_week_project'),
    )
