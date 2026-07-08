import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base

# Many-to-many association table between users and projects.
# WHY a Table object (not a Model): SQLAlchemy secondary tables used in
# relationship() don't need a full mapped class — a Table is sufficient.
project_members = Table(
    "project_members",
    Base.metadata,
    Column("project_id", String(36), ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id",    String(36), ForeignKey("users.id",    ondelete="CASCADE"), primary_key=True),
    Column("assigned_at", DateTime, default=datetime.utcnow, nullable=False),
)


class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    members = relationship("User", secondary=project_members, back_populates="projects")
    reports = relationship("Report", back_populates="project")
