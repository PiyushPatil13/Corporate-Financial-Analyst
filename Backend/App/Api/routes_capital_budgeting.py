from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.line_item_repository import LineRepository
from app.engine.capital_budgeting import CapitalBudgetingModule
from app.api.deps import get_current_user
from app.models.user import User
import numpy_financial as npf
from pydantic import BaseModel
from app.services.ownership_service import verify_statement_ownership

router = APIRouter()

@router.get("/capital_budgeting/{statement_id}")
def get_capital_budget(statement_id : str, db: Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    verify_statement_ownership(statement_id,current_user.id,db)
    line_repo = LineRepository(db)
    saved_items = line_repo.get_by_statement(statement_id)

    if not saved_items:
        raise HTTPException(status_code=404,detail="No line items found")

    data = {item.standardized_label : item.value for item in saved_items}
    module = CapitalBudgetingModule()
    result = module.run(data)

    return {
        "statement_id" : statement_id,
        "capital_budgeting_ratios" : result.values,
        "warnings" : result.warnings
    }


class NPVProfileRequest(BaseModel):
    cash_flows: list[float]
    rate_start: float = 0.0
    rate_end: float = 0.30
    rate_step: float = 0.02

@router.post("/capital_budgeting/npv_profile")
def get_npv_profile(request: NPVProfileRequest):
    rates = []
    npvs = []
    rate = request.rate_start
    while rate <= request.rate_end:
        npv = npf.npv(rate, request.cash_flows)
        rates.append(round(rate, 4))
        npvs.append(round(npv, 2))
        rate += request.rate_step

    try:
        irr = npf.irr(request.cash_flows)
    except Exception:
        irr = None

    return {"rates": rates, "npvs": npvs, "irr": irr}