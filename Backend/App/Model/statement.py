# this is for balance sheets ,income statements, financial statements
import uuid
from datetime import date
from sqlalchemy import Date,ForeignKey,String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.models.base import Base,TimestampMixin,UUIDPrimaryKeyMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.company import Company
    from app.models.line_item import LineItem
    from app.models.ratio_snapshot import RatioSnapshot

class Statement(Base,UUIDPrimaryKeyMixin,TimestampMixin):
    __tablename__ = "statements"
    company_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),ForeignKey("companies.id",ondelete="CASCADE"),index=True
    )
    statement_type : Mapped[str] = mapped_column(String(50))
    period_end : Mapped[date] = mapped_column(Date,index=True)
    period_label : Mapped[str] = mapped_column(String(20))
    source_filename : Mapped[str] = mapped_column(String(255),nullable=True)
    company : Mapped["Company"] = relationship(back_populates="statements")
    line_items: Mapped[list["LineItem"]] = relationship(
        back_populates="statement", cascade="all, delete-orphan"
    )
    ratio_snapshot: Mapped["RatioSnapshot"] = relationship(
        back_populates="statement", uselist=False, cascade="all, delete-orphan"
    )
    