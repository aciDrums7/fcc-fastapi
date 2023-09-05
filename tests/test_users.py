from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_hello_world():
    res = client.get("/")
    print(res.json())
    assert res.json() == "Hello World!"
    assert res.status_code == 200