import uuid
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from app.repositories.base_repository import BaseRepository
from app.models.scenario import Scenario

class ScenarioRepository(BaseRepository[Scenario]):
    def __init__(self, db : Session):
        super().__init__(db, Scenario)

    def get_by_statement(self,statement_id : uuid.UUID) -> list[Scenario]:
        return (
            self.db.query(Scenario).filter(Scenario.statement_id == statement_id)
        ).all()

    def get_by_type(self,statement_id : uuid.UUID,scenario_type : str) -> list[Scenario]:
        return (
            self.db.query(Scenario).filter(Scenario.statement_id == statement_id, Scenario.scenario_type == scenario_type)
        ).all()

    def get_worst_case(self,statement_id : uuid.UUID) -> Scenario | None:
        return(
            self.db.query(Scenario).filter(Scenario.statement_id == statement_id)
        ).order_by(Scenario.var_95.desc()).first()


    
    
    
