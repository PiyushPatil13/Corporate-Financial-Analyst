from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.repositories.recommendation_repository import RecommendationRepository
from app.models.recommendation import Recommendation

class RecommendationService:
    def __init__(self,db):
        self.Recommendation_repo = RecommendationRepository(db)

    def get_history(self,company_id) -> list[Recommendation]:
        return self.Recommendation_repo.get_recommendation_by_company(company_id)

    def get_current(self, company_id) -> Recommendation | None:
        return self.Recommendation_repo.get_latest_for_company(company_id)

    def is_stale(self, company_id, max_age_days = 90) -> bool :
        latest = self.get_current(company_id)
        if latest is None:
            return True

        age = datetime.now(timezone.utc) - latest.created_at
        return age.days > max_age_days
        