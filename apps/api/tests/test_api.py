def test_health(client):
    assert client.get("/healthz").json()["status"] == "ok"
    assert client.get("/readyz").status_code == 200


def test_list_empty(client):
    res = client.get("/applications")
    assert res.status_code == 200
    assert res.json() == []


def test_create_application(client):
    res = client.post("/applications", json={"company": "Acme", "role": "SRE"})
    assert res.status_code == 200
    body = res.json()
    assert body["company"] == "Acme"
    assert body["role"] == "SRE"
    assert body["status"] == "draft"
    assert isinstance(body["id"], int)
    listed = client.get("/applications").json()
    assert any(item["company"] == "Acme" for item in listed)
    assert listed[0]["id"] == body["id"]


def test_create_persists_across_list(client):
    client.post("/applications", json={"company": "Globex", "role": "Platform"})
    client.post("/applications", json={"company": "Initech", "role": "SRE"})
    companies = [item["company"] for item in client.get("/applications").json()]
    assert companies == ["Globex", "Initech"]
