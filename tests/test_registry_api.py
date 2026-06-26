from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_registries_endpoint():
    response = client.get("/registries")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_providers_endpoint():
    response = client.get("/providers")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_forecast_endpoint():
    response = client.get("/forecast")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_copilot_why():
    response = client.get("/copilot/why")

    assert response.status_code == 200

    data = response.json()

    assert "decision" in data
    assert "confidence" in data
    assert "reasons" in data
