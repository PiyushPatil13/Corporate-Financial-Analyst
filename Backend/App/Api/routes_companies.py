from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.company import Company
from app.repositories.company_repository import CompanyRepository
from app.repositories.statement_repository import StatementRepository
from app.repositories.statement_repository import StatementRepository
from app.services.ownership_service import verify_company_ownership
from app.engine.growth import GrowthModule
from app.repositories.line_item_repository import LineRepository

class CompanyCreate(BaseModel):
    name: str
    sector: str | None = None
    ticker: str | None = None


router = APIRouter()


@router.post("/companies")
def create_company(
    request: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    company_repo = CompanyRepository(db)
    company = company_repo.create(Company(
        user_id=current_user.id,
        name=request.name,
        sector=request.sector,
        ticker=request.ticker,
    ))
    return {"company_id": str(company.id), "name": company.name}


@router.get("/companies")
def list_my_companies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    company_repo = CompanyRepository(db)
    companies = company_repo.get_by_user(current_user.id)
    return [{"company_id": str(c.id), "name": c.name, "ticker": c.ticker} for c in companies]



@router.get("/companies/{company_id}/statements")
def list_company_statements(
    company_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from app.services.ownership_service import verify_company_ownership
    verify_company_ownership(company_id, current_user.id, db)

    statement_repo = StatementRepository(db)
    statements = statement_repo.get_by_company(company_id)
    return [
        {"statement_id": str(s.id), "period_label": s.period_label, "statement_type": s.statement_type, "period_end": str(s.period_end)}
        for s in statements
    ]


@router.get("/companies/{company_id}/statements")
def list_company_statements(
    company_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_company_ownership(company_id, current_user.id, db)
    statement_repo = StatementRepository(db)
    statements = statement_repo.get_by_company(company_id)
    return [
        {"statement_id": str(s.id), "period_label": s.period_label, "statement_type": s.statement_type, "period_end": str(s.period_end)}
        for s in statements
    ]

@router.get("/companies/{company_id}/growth")
def get_growth(company_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verify_company_ownership(company_id, current_user.id, db)

    statement_repo = StatementRepository(db)
    line_repo = LineRepository(db)

    statements = statement_repo.get_by_company(company_id)
    sorted_statements = sorted(statements, key=lambda s: s.period_end)

    if len(sorted_statements) < 2:
        return {"revenue_growth": None, "net_income_growth": None, "note": "Need at least 2 statements to compute growth"}

    previous_stmt, current_stmt = sorted_statements[-2], sorted_statements[-1]

    def get_metric(statement_id, label):
        items = line_repo.get_by_label(statement_id, label)
        return items.value if items else None

    data = {
        "current_revenue": get_metric(current_stmt.id, "revenue"),
        "previous_revenue": get_metric(previous_stmt.id, "revenue"),
        "current_net_income": get_metric(current_stmt.id, "net_income"),
        "previous_net_income": get_metric(previous_stmt.id, "net_income"),
    }

    module = GrowthModule()
    result = module.run(data)
    return result.values