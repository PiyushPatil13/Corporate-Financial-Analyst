import uuid
from sqlalchemy.orm import mapped_column,Mapped,relationship
from sqlalchemy import Float,ForeignKey
from sqlalchemy.dialects.postgresql import JSONB,UUID
from app.models.base import Base,TimestampMixin,UUIDPrimaryKeyMixin
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.statement import Statement

class RatioSnapshot(Base,UUIDPrimaryKeyMixin,TimestampMixin):
    __tablename__ = "ratio_snapshots"

    statement_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("statements.id",ondelete="CASCADE"),unique=True
    )
    current_ratio : Mapped[float] = mapped_column(Float,nullable=True)
    quick_ratio : Mapped[float] = mapped_column(Float,nullable=True)

    debt_to_equity : Mapped[float] = mapped_column(Float,nullable=True)
    debt_to_ebitda : Mapped[float] = mapped_column(Float,nullable=True)
    interest_coverage : Mapped[float] = mapped_column(Float,nullable=True)

    dso : Mapped[float] = mapped_column(Float,nullable=True)
    dio : Mapped[float] = mapped_column(Float,nullable=True)
    dpo : Mapped[float] = mapped_column(Float,nullable=True)
    cash_conversion_cycle : Mapped[float] = mapped_column(Float,nullable=True)

    gross_margin : Mapped[float] = mapped_column(Float,nullable=True)
    operating_margin: Mapped[float] = mapped_column(Float,nullable=True)
    net_margin : Mapped[float] = mapped_column(Float,nullable=True)
    roe : Mapped[float] = mapped_column(Float,nullable=True)
    roic : Mapped[float] = mapped_column(Float,nullable=True)

    financial_health_score : Mapped[Float] = mapped_column(Float,nullable=True)
    raw_breakdown : Mapped[float] = mapped_column(Float,nullable=True)

    statement : Mapped["Statement"] = relationship(back_populates="ratio_snapshot")


