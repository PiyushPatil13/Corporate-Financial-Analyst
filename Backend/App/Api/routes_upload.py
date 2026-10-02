import shutil
import tempfile
from datetime import date
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.ingestion_service import IngestionService
from app.api.deps import get_current_user
from app.models.user import User
from app.repositories.company_repository import CompanyRepository

router = APIRouter()

@router.post("/upload")
def upload_statement(
    company_id : str,
    period_end : date,
    file : UploadFile = File(...),
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):

    company_repo = CompanyRepository(db)
    company = company_repo.get(company_id)

    if company is None or company.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have access to this company")

    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        shutil.copyfileobj(file.file,tmp)
        tmp_path = tmp.name

    service = IngestionService(db)


    results = service.ingest_file(tmp_path, company_id, period_end)

    return {
        "statements": [
            {
                "statement_id": str(statement.id),
                "period_label": statement.period_label,
                "statement_type": statement.statement_type,
                "validation": {
                    "is_valid": validation_result.is_valid,
                    "errors": validation_result.errors,
                    "warnings": validation_result.warnings,
                },
            }
            for statement, validation_result in results
        ]
    }