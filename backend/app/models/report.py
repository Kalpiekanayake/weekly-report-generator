import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Date, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="RESTRICT"), nullable=False, index=True)

    # ISO Monday date that marks the start of the reporting week
    week_start_date = Column(Date, nullable=False, index=True)

    # Required report sections
    tasks_completed = Column(String, nullable=False)
    tasks_planned = Column(String, nullable=False)
    blockers = Column(String, nullable=False)

    # Optional fields
    hours_worked = Column(Float, nullable=True)
    notes = Column(String, nullable=True)

    # Lifecycle: 'draft' | 'submitted'
    status = Column(String(50), default="draft", nullable=False)
    submitted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="reports")
    project = relationship("Project", back_populates="reports")

    # One report per user per project per week
    __table_args__ = (
        UniqueConstraint("user_id", "week_start_date", "project_id", name="uq_user_week_project"),
    )
