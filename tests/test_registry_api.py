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


def test_copilot_executive_snapshot_post():
    response = client.post("/copilot/executive-snapshot")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "executive snapshot completed"
    assert "snapshot" in data
    assert "snapshot_id" in data["snapshot"]
    assert "risk_score" in data["snapshot"]
    assert "risk_severity" in data["snapshot"]


def test_copilot_executive_recommendation():
    response = client.get("/copilot/executive-recommendation")

    assert response.status_code == 200

    data = response.json()

    assert data["summary"]["status"] == (
        "executive recommendation available"
    )

    assert "priority" in data["summary"]

    recommendation = data["recommendation"]

    assert "action" in recommendation
    assert "reason" in recommendation
    assert "owner" in recommendation


def test_copilot_executive_decision_center():
    response = client.get("/copilot/executive-decision-center")

    assert response.status_code == 200

    data = response.json()

    assert data["summary"]["status"] == (
        "executive decision center available"
    )

    assert "risk" in data
    assert "recommendation" in data
    assert "changes" in data
    assert "snapshots" in data
    assert "executive_intelligence" in data

    assert "kpis" in data

    assert "snapshot_count" in data["kpis"]
    assert "change_events" in data["kpis"]
    assert "risk_score" in data["kpis"]
    assert "priority" in data["kpis"]
