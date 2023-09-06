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

test_email = "test@email.com"
test_password = "testPassword1"


@pytest.fixture(name="session")
def session():
    print("session fixture run")
    Base.metadata.drop_all(bind=Engine)
    Base.metadata.create_all(bind=Engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(name="client")
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


@pytest.fixture
def test_user(client):
    new_user_data = {"email": test_email, "password": test_password}
    res = client.post("/users", json=new_user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["plain_password"] = new_user_data["password"]
    return new_user
