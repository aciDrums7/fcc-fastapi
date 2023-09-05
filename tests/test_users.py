from fastapi.testclient import TestClient
from app.main import app
from app.schemas.users_schemas import UserOut
from app.utils.password_utils import verify_password

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
