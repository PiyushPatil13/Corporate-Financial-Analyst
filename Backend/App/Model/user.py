from sqlalchemy import String
from sqlalchemy.orm import mapped_column,Mapped,relationship
from app.models.base import Base,TimestampMixin,UUIDPrimaryKeyMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.copilot_session import CopilotSession
    from app.models.company import Company

class User(Base,UUIDPrimaryKeyMixin,TimestampMixin):
    __tablename__ = "users"
    companies: Mapped[list["Company"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    email : Mapped[str] = mapped_column(String(255),unique=True,index=True,nullable=False)
    hashed_password : Mapped[str] = mapped_column(String(255),nullable=False)
    full_name : Mapped[str] = mapped_column(String(255),nullable=True)
    role : Mapped[str] = mapped_column(String(50),default="analyst")

    copilot_sessions : Mapped[list["CopilotSession"]] = relationship(
        back_populates="user",cascade="all, delete-orphan"
    )
    