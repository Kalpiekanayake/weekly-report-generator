import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Uuid
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)  # 'member' or 'manager'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")
    ai_chats = relationship("AIChatHistory", back_populates="user", cascade="all, delete-orphan")
    
    # Many-to-many relationship with projects via project_members table
    projects = relationship("Project", secondary="project_members", back_populates="members")
