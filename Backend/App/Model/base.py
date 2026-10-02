import uuid
from datetime import datetime
from sqlalchemy import Boolean,DateTime,func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

class Base(DeclarativeBase):
    pass

# this will create random primary keys and not in 1,2,3 order to safeguard count of entities
class UUIDPrimaryKeyMixin:
    id:Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),primary_key=True,default=uuid.uuid4
    )

# basic timestamp class for new entry or update in database of postgres to get accurate time
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),server_default=func.now(),onupdate=func.now()
    )

class SoftDeleteMixin:
    is_deleted:Mapped[Boolean] = mapped_column(
        Boolean,default=False,nullable=False
    )



