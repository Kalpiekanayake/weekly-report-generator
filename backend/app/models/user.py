import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    # WHY String(36): Using a plain string UUID is compatible with both
    # PostgreSQL and the SQLite fallback, avoiding dialect-specific types.
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    # role: either 'member' or 'manager'
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships — lazy-loaded by default; cascade ensures cleanup on delete
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")
    ai_chats = relationship("AIChatHistory", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", secondary="project_members", back_populates="members")
