import pytest
from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


@pytest.fixture
def job_payload():
    return {
        "target": "dataset-001",
        "config": {"param": "value"},
        "priority": "high",
    }


def test_submit_job_success(job_payload):
    response = client.post("/api/v1/jobs", json=job_payload)
    assert response.status_code == 201
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "queued"


def test_duplicate_job_id(job_payload):
    # First submission
    response1 = client.post("/api/v1/jobs", json=job_payload)
    assert response1.status_code == 201

    # Second submission with same payload should conflict
    response2 = client.post("/api/v1/jobs", json=job_payload)
    assert response2.status_code == 409
    assert response2.json()["detail"] == "Duplicate job_id"