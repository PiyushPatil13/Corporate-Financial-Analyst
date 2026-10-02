from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.statement_repository import StatementRepository
from app.repositories.company_repository import CompanyRepository

def verify_statement_ownership(statement_id : str, user_id, db : Session) -> None:
    statement_repo = StatementRepository(db)
    company_repo = CompanyRepository(db)

    statement = statement_repo.get(statement_id)
    if statement is None:
        raise HTTPException(status_code=404, detail="Statement not found")

    company = company_repo.get(statement.company_id)
    if company is None or company.user_id != user_id:
        raise HTTPException(status_code=403, detail="You do not have access to this statement")

def verify_company_ownership(company_id: str, user_id, db: Session) -> None:
    company_repo = CompanyRepository(db)
    company = company_repo.get(company_id)

    if company is None or company.user_id != user_id:
        raise HTTPException(status_code=403, detail="You do not have access to this company")