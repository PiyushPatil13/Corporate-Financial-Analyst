from typing import TYPE_CHECKING
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.statement import Statement
    from app.models.user import User

class Company(Base,UUIDPrimaryKeyMixin,TimestampMixin,SoftDeleteMixin):
    __tablename__ = "companies"
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    name:Mapped[str] = mapped_column(String(255),nullable=False)
    sector:Mapped[str] = mapped_column(String(100),nullable=True)
    ticker:Mapped[str] = mapped_column(String(100),nullable=True)
    timestamp : Mapped[str] = mapped_column(String(50),nullable=True)
    user : Mapped["User"] = relationship(back_populates="companies")
    statements:Mapped[list["Statement"]] = relationship(
        back_populates="company",cascade="all, delete-orphan"
    )