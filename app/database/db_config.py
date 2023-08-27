""" DB Config """
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings


DB_URL = (
    f"postgresql://"
    f"{settings.DB_USERNAME}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOSTNAME}:{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)

Engine = create_engine(
    DB_URL,
    # connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

Base = declarative_base()
# ? Porkaround to make SQLAlchemy create the "votes" table
# ! Don't move this import, needs to stay after the Base var declaration!
# from app.models.votes_model import VoteModel


# Dependency
def get_db_session():
    """Return database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
