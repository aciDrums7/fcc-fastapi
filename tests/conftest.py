import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.db_config import get_db, Base
from app.main import app
from app.settings import settings
from app.authentication import oauth2_service
from app.models.posts_model import PostModel

DB_TEST_URL = (
    f"postgresql://"
    f"{settings.DB_USERNAME}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOSTNAME}:{settings.DB_PORT}/"
    f"{settings.DB_TEST_NAME}"
)

Engine = create_engine(DB_TEST_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

test_email = "test@email.com"
test_email2 = "test2@email.com"
test_password = "testPassword1"


@pytest.fixture(name="session")
def session():
    print("\n\nNEW SESSION\n")
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


@pytest.fixture(name="test_user")
def test_user(client):
    new_user_data = {"email": test_email, "password": test_password}
    res = client.post("/users", json=new_user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["plain_password"] = new_user_data["password"]
    return new_user


@pytest.fixture(name="test_user2")
def test_user2(client):
    new_user_data = {"email": test_email2, "password": test_password}
    res = client.post("/users", json=new_user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["plain_password"] = new_user_data["password"]
    return new_user


@pytest.fixture(name="token")
def token(test_user):
    return oauth2_service.create_access_token({"user_id": test_user["id"]})


@pytest.fixture(name="authorized_client")
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture(name="test_posts")
def test_posts(session, test_user, test_user2):
    post_list = [
        {
            "title": "first title",
            "content": "1st content",
            "owner_id": test_user["id"],
        },
        {
            "title": "second title",
            "content": "2nd content",
            "owner_id": test_user["id"],
        },
        {
            "title": "third title",
            "content": "3rd content",
            "owner_id": test_user["id"],
        },
        {
            "title": "fourth title",
            "content": "4th content",
            "owner_id": test_user2["id"],
        },
    ]

    post_model_list = [PostModel(**post) for post in post_list]

    session.add_all(post_model_list)
    session.commit()

    db_post_list = session.query(PostModel).all()
    return db_post_list
