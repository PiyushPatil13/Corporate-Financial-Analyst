import uuid
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User


class CopilotSession(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "copilot_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), index=True
    )

    user: Mapped["User"] = relationship(back_populates="copilot_sessions")
    messages: Mapped[list["CopilotMessage"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", order_by="CopilotMessage.created_at"
    )


class CopilotMessage(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "copilot_messages"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("copilot_sessions.id", ondelete="CASCADE"), index=True
    )
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)

    session: Mapped["CopilotSession"] = relationship(back_populates="messages")