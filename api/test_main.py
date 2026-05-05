import os
import sys
from unittest.mock import MagicMock, patch

os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("REDIS_PORT", "6379")
os.environ.setdefault("REDIS_PASSWORD", "")

import pytest


@pytest.fixture
def mock_redis():
    mock = MagicMock()
    mock.ping.return_value = True
    mock.rpush.return_value = 1
    mock.hset.return_value = 1
    mock.hget.return_value = b"queued"
    return mock


@pytest.fixture
def client(mock_redis):
    with patch("main.redis.Redis", return_value=mock_redis):
        from fastapi.testclient import TestClient
        import main
        return TestClient(main.app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_check_error(client, mock_redis):
    mock_redis.ping.side_effect = Exception("Connection failed")
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "error"


def test_create_job(client):
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) == 36


def test_get_job(client, mock_redis):
    mock_redis.hget.return_value = b"completed"
    response = client.get("/jobs/test-id")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_get_job_not_found(client, mock_redis):
    mock_redis.hget.return_value = None
    response = client.get("/jobs/missing")
    assert response.status_code == 200
    assert response.json()["error"] == "not found"