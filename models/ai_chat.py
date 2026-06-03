from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class AIChatMessage(Base):
    """Holds individual messages from AI Consultation or AI Chat."""
    __tablename__ = "ai_chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)  # "user" or "assistant"
    content: Mapped[str] = mapped_column(Text, nullable=False)
    chat_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "consultation" or "chat"
    session_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # to group messages

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationship to user
    user = relationship("User")

    def __repr__(self) -> str:
        return f"<AIChatMessage id={self.id} user_id={self.user_id} role={self.role} chat_type={self.chat_type}>"
