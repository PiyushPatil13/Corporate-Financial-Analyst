from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.line_item_repository import LineRepository
from app.engine.recommendation import RecommendationModule
from app.api.deps import get_current_user
from app.models.user import User
from app.services.ownership_service import verify_statement_ownership
from app.services.analysis_service import AnalysisService
from app.repositories.recommendation_repository import RecommendationRepository
from app.genai.memo_generator import MemoGenerator


router = APIRouter()

@router.get("/Recommendation/{statement_id}")
def get_recommendation(statement_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verify_statement_ownership(statement_id, current_user.id, db)

    rec_repo = RecommendationRepository(db)
    recommendations = rec_repo.get_by_statement(statement_id)

    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendation generated yet for this statement")

    latest = recommendations[-1]
    return {
        "statement_id": statement_id,
        "recommended_action": latest.recommended_action,
        "supporting_metrics": latest.supporting_metrics,
    }

@router.post("/recommendation/{statement_id}/generate")
def generate_recommendation(
    statement_id: str,
    company_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_statement_ownership(statement_id, current_user.id, db)

    service = AnalysisService(db)
    recommendation = service.analyze_statement(company_id, statement_id)

    return {
        "recommended_action": recommendation.recommended_action,
        "supporting_metrics": recommendation.supporting_metrics,
    }


@router.get("/recommendation/{statement_id}/memo")
def get_recommendation_memo(statement_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verify_statement_ownership(statement_id, current_user.id, db)

    rec_repo = RecommendationRepository(db)
    recommendations = rec_repo.get_by_statement(statement_id)

    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendation generated yet")

    latest = recommendations[-1]
    generator = MemoGenerator()
    memo_text = generator.generate_memo(latest)

    return {"memo": memo_text}