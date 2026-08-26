from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/healthz").json()["status"] == "ok"
    assert client.get("/readyz").status_code == 200


def test_create_application():
    res = client.post("/applications", json={"company": "Acme", "role": "SRE"})
    assert res.status_code == 200
    assert any(item["company"] == "Acme" for item in client.get("/applications").json())
