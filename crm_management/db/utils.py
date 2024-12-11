import os

from sqlalchemy import create_engine, Engine

from crm_management.db.orm_base import Base


def init_db() -> Engine:
    db_url = os.getenv("DATABASE_URL")
    if db_url is None:
        raise ValueError("No database URL found in the env variables.")
    engine = create_engine(db_url, echo=True)
    Base.metadata.create_all(bind=engine)
    return engine
