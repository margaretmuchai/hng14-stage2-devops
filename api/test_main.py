import pytest
from fastapi.testclient import TestClient
import main


@pytest.fixture
def client():
    return TestClient(main.app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_check_error(client):
    def raise_error():
        raise Exception("Connection failed")
    main.r.ping = raise_error
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "error"


def test_create_job(client):
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) == 36


def test_get_job(client):
    main.r._data["job:test-id:status"] = "completed"
    response = client.get("/jobs/test-id")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_get_job_not_found(client):
    response = client.get("/jobs/missing")
    assert response.status_code == 200
    assert response.json()["error"] == "not found"
