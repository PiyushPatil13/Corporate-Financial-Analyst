from sqlalchemy.orm import Session
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.models.statement import Statement
from app.repositories.base_repository import BaseRepository

class StatementRepository(BaseRepository[Statement]):
    def __init__(self, db:Session):
        super().__init__(db, Statement)

    def get_statement_by_type(self,statement_type:str,company_id: uuid.UUID) -> Statement | None:
        return (
            self.db.query(Statement).filter(Statement.statement_type == statement_type)
        ).first()

    # get statement by company 
    def get_by_company(self,company_id : uuid.UUID) -> list[Statement]:
        return  (
            self.db.query(Statement).filter(Statement.company_id == company_id)
        ).all()

    # get by company name and its type 
    def get_by_company_and_type(self,company_id : uuid.UUID,statement_type:str) -> list[Statement]:
        return (
            self.db.query(Statement).filter(Statement.company_id == company_id,Statement.statement_type==statement_type)
        ).all()

    # this would fetch the latest statement of any company 
    def get_latest_by_type(self,company_id : uuid.UUID,statement_type:str) -> Statement | None:
        return (
             self.db.query(Statement).filter(Statement.company_id == company_id,Statement.statement_type==statement_type)
        ).order_by(Statement.period_end.desc()).first()

    