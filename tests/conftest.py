import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.db_config import get_db, Base
from app.main import app
from app.config import settings

DB_TEST_URL = (
    f"postgresql://"
    f"{settings.DB_USERNAME}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOSTNAME}:{settings.DB_PORT}/"
    f"{settings.DB_TEST_NAME}"
)

Engine = create_engine(
    DB_TEST_URL,
    # connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=Engine)
    Base.metadata.create_all(bind=Engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    # 1 yield -> run code before running tests
    yield TestClient(app)
    # 2 yield -> run code after tests finish