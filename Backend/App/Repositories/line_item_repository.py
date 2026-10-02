import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.models.line_item import LineItem
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session

class LineRepository(BaseRepository[LineItem]):
    def __init__(self, db:Session):
        super().__init__(db,LineItem)

    def get_by_statement(self,statement_id:uuid.UUID) -> list[LineItem]:
        return (
            self.db.query(LineItem).filter(LineItem.statement_id == statement_id)
        ).all()

    def get_by_label(self,statement_id:uuid.UUID,standardized_label:str) -> LineItem | None:
        return (
            self.db.query(LineItem).filter(LineItem.statement_id == statement_id, LineItem.standardized_label == standardized_label)
        ).first()

    def get_low_confidence_mappings(self,statement_id:uuid.UUID,threshold:float = 0.7) -> list[LineItem]:
        return (
            self.db.query(LineItem).filter(LineItem.statement_id == statement_id, LineItem.mapping_confidence < threshold)
        ).all()
    

    
