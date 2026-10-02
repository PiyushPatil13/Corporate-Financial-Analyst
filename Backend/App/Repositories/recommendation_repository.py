from sqlalchemy.orm import Session
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.models.recommendation import Recommendation
from app.repositories.base_repository import BaseRepository

class RecommendationRepository(BaseRepository[Recommendation]):
    def __init__(self, db:Session):
        super().__init__(db, Recommendation)

    def get_recommendation_by_company(self,company_id:uuid.UUID) -> list[Recommendation]:
        return (
            self.db.query(Recommendation).filter(Recommendation.company_id==company_id)
        ).all()

    def get_by_statement(self,statement_id:uuid.UUID) -> list[Recommendation]:
        return (
            self.db.query(Recommendation).filter(Recommendation.statement_id==statement_id)
        ).all()

    def get_latest_for_company(self,company_id:uuid.UUID) -> Recommendation | None:
        return (
            self.db.query(Recommendation).filter(Recommendation.company_id==company_id)
        ).order_by(Recommendation.created_at.desc()).first()

    def get_by_action(self,company_id:uuid.UUID,action:str) -> list[Recommendation]:
        return (
            self.db.query(Recommendation).filter(Recommendation.company_id==company_id,Recommendation.recommended_action==action)
        ).order_by(Recommendation.created_at.desc()).all()

    