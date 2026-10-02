from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.copilot_service import CopilotService
from app.schemas.copilot_schema import CopilotQuestion
from app.api.deps import get_current_user
from app.models.user import User
from app.services.ownership_service import verify_company_ownership

router = APIRouter()


@router.post("/companies/{company_id}/copilot")
def ask_copilot(
    company_id: str,
    request: CopilotQuestion,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_company_ownership(company_id, current_user.id, db)

    service = CopilotService(db)

    answer = service.ask(
        company_id,
        request.statement_id,
        request.question
    )

    if answer is None:
        raise HTTPException(
            status_code=404,
            detail="No recommendation history found for this company"
        )

    return {
        "company_id": company_id,
        "question": request.question,
        "answer": answer
    }