from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from core.config import settings

connection_string = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_SERVER}/{settings.DB_NAME}"
db_engine = create_engine(connection_string, echo=True)

if not database_exists(db_engine.url):
    create_database(db_engine.url)

DatabaseSession = sessionmaker(bind=db_engine, autocommit=False, autoflush=False)

Base = declarative_base()


def db_session():
    session = DatabaseSession()
    try:
        yield session
    finally:
        session.close()


def setup_database():
    Base.metadata.create_all(bind=db_engine)


def teardown_database():
    db_engine.dispose()


__all__ = ["db_session"]
