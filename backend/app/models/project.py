import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Uuid, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base

# Many-to-many relationship join table
project_members = Table(
    "project_members",
    Base.metadata,
    Column("project_id", Uuid, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", Uuid, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("assigned_at", DateTime, default=datetime.utcnow, nullable=False)
)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    members = relationship("User", secondary=project_members, back_populates="projects")
    reports = relationship("Report", back_populates="project")
