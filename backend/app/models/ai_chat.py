import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Uuid, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class AIChatHistory(Base):
    __tablename__ = "ai_chat_history"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    prompt = Column(String, nullable=False)
    response = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="ai_chats")
