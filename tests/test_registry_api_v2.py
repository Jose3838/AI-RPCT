from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] in {"ok", "degraded"}


def test_pipeline_endpoint():
    response = client.get("/pipeline")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_dynamic_registry_endpoint():
    response = client.get("/registry/feature_store")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_unknown_registry_returns_404():
    response = client.get("/registry/does_not_exist")

    assert response.status_code == 404
