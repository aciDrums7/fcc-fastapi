import pytest
from app.schemas.token_schemas import Token
from tests.conftest import client
from app.schemas.users_schemas import UserOut
from app.utils.password_utils import verify_password


@pytest.fixture
def test_user(client):
    new_user_data = {"email": "testuser@email.com", "password": "testPassword1"}
    res = client.post("/users", json=new_user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["plain_password"] = new_user_data["password"]
    return new_user


def test_hello_world(client):
    res = client.get("/")
    print(res.json())
    assert res.json() == "Hello World!"
    assert res.status_code == 200


def test_create_user(client):
    test_email = "test@email.com"
    test_password = "testpassword"
    res = client.post("/users", json={"email": test_email, "password": test_password})
    print(res.json())
    new_user = UserOut(**res.json())
    assert new_user.email == test_email
    assert verify_password(test_password, new_user.password)
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["plain_password"]},
    )
    print(res.json())
    new_token = Token(**res.json())
    assert res.status_code == 200
