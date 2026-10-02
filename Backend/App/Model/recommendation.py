import uuid
from typing import TYPE_CHECKING
from sqlalchemy import Float,ForeignKey,String,Text
from sqlalchemy.dialects.postgresql import JSONB,UUID
from sqlalchemy.orm import mapped_column,Mapped,relationship
from app.models.base import Base,UUIDPrimaryKeyMixin,TimestampMixin

if TYPE_CHECKING:
    from app.models.scenario import Scenario


class Recommendation(Base,UUIDPrimaryKeyMixin,TimestampMixin):
    __tablename__ = "recommendations"
    company_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),ForeignKey("companies.id",ondelete="CASCADE"),index = True
    )
    statement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("statements.id", ondelete="CASCADE")
    )
    scenario_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),ForeignKey('scenarios.id'),nullable=True
    )

    recommended_action : Mapped[str] = mapped_column(String(50))
    allocated_amount : Mapped[float] =  mapped_column(Float,nullable=True)
    rationable : Mapped[str] = mapped_column(Text,nullable=True)
    supporting_metrics : Mapped[dict] = mapped_column(JSONB,nullable=True)
    scenario : Mapped["Scenario"] = relationship(back_populates="recommendations")
