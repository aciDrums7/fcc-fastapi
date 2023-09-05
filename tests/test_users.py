from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database.db_config import get_db, Base
from app.schemas.users_schemas import UserOut
from app.utils.password_utils import verify_password

DB_URL = (
    f"postgresql://"
    f"{settings.DB_USERNAME}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOSTNAME}:{settings.DB_PORT}/"
    f"{settings.DB_TEST_NAME}"
)
Engine = create_engine(
    DB_URL,
    # connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)


def override_get_db():
    """Return database session"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=Engine)

client = TestClient(app)


def test_hello_world():
    res = client.get("/")
    print(res.json())
    assert res.json() == "Hello World!"
    assert res.status_code == 200


def test_create_user():
    test_email = "test@email.com"
    test_password = "testpassword"
    res = client.post("/users", json={"email": test_email, "password": test_password})
    print(res.json())
    new_user = UserOut(**res.json())
    assert new_user.email == test_email
    assert verify_password(test_password, new_user.password)
    assert res.status_code == 201
