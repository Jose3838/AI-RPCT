from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_limit():
    response = client.get("/registry/feature_store?limit=1")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_offset():
    response = client.get("/registry/feature_store?offset=1")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_sort():
    response = client.get("/registry/feature_store?sort=vendor")

    assert response.status_code == 200


def test_invalid_sort():
    response = client.get("/registry/feature_store?sort=unknown_column")

    assert response.status_code == 400
