from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.line_item_repository import LineRepository
from app.engine.ratios import RatiosModule
from app.api.deps import get_current_user
from app.models.user import User
from app.services.ownership_service import verify_statement_ownership

router = APIRouter()

@router.get("/ratios/{statement_id}")
def get_ratios(statement_id : str, db: Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    verify_statement_ownership(statement_id,current_user.id,db)
    line_repo = LineRepository(db)
    saved_items = line_repo.get_by_statement(statement_id)

    if not saved_items:
        raise HTTPException(status_code=404, detail="No line items found for this statement")

    data = {item.standardized_label : item.value for item in saved_items}

    module = RatiosModule()
    result = module.run(data)

    return {
        "statement_id": statement_id,
        "ratios": result.values,
        "warnings": result.warnings,
    }

@router.get("/line_items/{statement_id}")
def get_line_items(statement_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verify_statement_ownership(statement_id, current_user.id, db)
    line_repo = LineRepository(db)
    items = line_repo.get_by_statement(statement_id)
    return [{"label": i.standardized_label, "value": i.value, "confidence": i.mapping_confidence} for i in items]