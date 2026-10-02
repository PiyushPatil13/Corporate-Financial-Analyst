from app.db.session import engine
from app.models.base import Base

from app.models import company
from app.models import statement
from app.models import line_item
from app.models import ratio_snapshot
from app.models import scenario
from app.models import recommendation
from app.models import user
from app.models import copilot_session


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    print("Tables created.")


if __name__ == "__main__":
    init_db()