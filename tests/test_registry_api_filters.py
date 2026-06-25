from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_registry_filter_by_vendor():
    response = client.get(
        "/registry/feature_store",
        params={
            "key": "vendor",
            "value": "NVIDIA",
        },
    )

    assert response.status_code == 200
    rows = response.json()

    assert isinstance(rows, list)
    assert len(rows) >= 1
    assert all(row["vendor"] == "NVIDIA" for row in rows)


def test_registry_filter_requires_key_and_value():
    response = client.get(
        "/registry/feature_store",
        params={
            "key": "vendor",
        },
    )

    assert response.status_code == 400


def test_registry_filter_rejects_unknown_key():
    response = client.get(
        "/registry/feature_store",
        params={
            "key": "does_not_exist",
            "value": "x",
        },
    )

    assert response.status_code == 400
