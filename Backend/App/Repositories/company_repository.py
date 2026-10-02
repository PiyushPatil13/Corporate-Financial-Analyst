from sqlalchemy.orm import Session
from app.models.company import Company
from app.repositories.base_repository import BaseRepository

class CompanyRepository(BaseRepository[Company]):
    def __init__(self,db:Session):
        super().__init__(db,Company)

    # get the company by the ticker 
    def get_by_ticker(self,ticker:str) -> Company | None:
        return (
            self.db.query(Company).filter(Company.ticker == ticker,Company.is_deleted.is_(False))
        ).first()

    # get the active list of companies
    def list_active(self) -> list[Company]:
        return (
            self.db.query(Company).filter(Company.is_deleted.is_(False))
        ).all()

    # get the company by name itself
    def search_by_name(self,name_query:str) -> list[Company]:
        return (
            self.db.query(Company).filter(Company.name.ilike(f"%{name_query}%"),Company.is_deleted.is_(False))
        ).all()

    # or get by sector
    def get_by_sector(self,sector:str) -> list[Company]:
        return(
            self.db.query(Company).filter(Company.sector==sector,Company.is_deleted.is_(False))
        ).all()

    def get_by_user(self, user_id) -> list[Company]:
        return (
            self.db.query(Company)
            .filter(Company.user_id == user_id, Company.is_deleted.is_(False))
            .all()
        )
    

    