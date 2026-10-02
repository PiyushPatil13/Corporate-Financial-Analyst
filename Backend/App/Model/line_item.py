import uuid
from sqlalchemy import Float,ForeignKey,Index,String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.models.base import Base,UUIDPrimaryKeyMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.statement import Statement

class LineItem(Base,UUIDPrimaryKeyMixin):
    __tablename__ = "line_items"
    __table_args__ = (
        Index("ix_line_items_statement_standard","statement_id","standardized_label"),
    )
    statement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),ForeignKey("statements.id",ondelete="CASCADE"),index=True
    )
    raw_label: Mapped[str] = mapped_column(String(255))
    standardized_label: Mapped[str] = mapped_column(String(100), index=True)
    value: Mapped[float] = mapped_column(Float)
    mapping_confidence: Mapped[float] = mapped_column(Float, default=1.0)

    statement: Mapped["Statement"] = relationship(back_populates="line_items")