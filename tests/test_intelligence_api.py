from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_unified_intelligence_api():
    response = client.get("/copilot/intelligence")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert "decision" in data
    assert "planner" in data
    assert "graph" in data
    assert "cycle" in data
    assert "intelligence" in data


def test_intelligence_cycle_api():
    response = client.get("/copilot/intelligence-cycle")

    assert response.status_code == 200

    data = response.json()

    assert "cycle" in data
    assert "memory" in data
    assert "workflow" in data
    assert "pipeline" in data
    assert "simulation" in data
