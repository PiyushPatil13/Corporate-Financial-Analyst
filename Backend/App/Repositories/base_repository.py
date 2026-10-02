import uuid
from typing import Generic, TypeVar
from sqlalchemy.orm import Session
from app.models.base import Base

ModelType = TypeVar("ModelType",bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self,db:Session,model: type[ModelType]):
        self.db = db
        self.model = model

    def get(self,id:uuid.UUID) -> ModelType | None:
        return self.db.query(self.model).filter(self.model.id==id).first()

    def list(self,**filters) -> list[ModelType]:
        query = self.db.query(self.model)
        for field, value in filters.items():
            query = query.filter(getattr(self.model,field)==value)
        return query.all()

    def create(self,obj:ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, obj: ModelType) -> ModelType:
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def soft_delete(self,id:uuid.UUID) -> None:
        obj = self.get(id)
        if obj is not None and hasattr(obj,"is_deleted"):
            obj.is_deleted = True
            self.db.commit()


    