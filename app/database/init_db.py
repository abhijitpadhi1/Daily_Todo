from app.database.db import engine, Base
from app.database import models  # noqa: F401

def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)
