import uuid
from sqlalchemy.orm import mapped_column,Mapped,relationship
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy import Float,ForeignKey,String
from app.models.base import Base,UUIDPrimaryKeyMixin,TimestampMixin
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.recommendation import Recommendation

class Scenario(Base,UUIDPrimaryKeyMixin,TimestampMixin):
    __tablename__ = "scenarios"

    statement_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),ForeignKey("statements.id",ondelete="CASCADE"),index=True
    )

    scenario_type : Mapped[str] = mapped_column(String(50))
    label : Mapped[str] = mapped_column(String(100))
    assumptions : Mapped[dict] = mapped_column(JSONB)
    results : Mapped[dict] = mapped_column(JSONB)
    var_95 : Mapped[float] = mapped_column(Float,nullable=True)
    expected_npv : Mapped[float] = mapped_column(Float,nullable=True)
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="scenario")
