from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_pause_pipeline():
    response = client.put("/api/pipelines/1/pause")
    assert response.status_code == 200
    assert response.json() == {"message": "Pipeline paused successfully"}

def test_cancel_pipeline():
    response = client.put("/api/pipelines/1/cancel")
    assert response.status_code == 200
    assert response.json() == {"message": "Pipeline cancelled successfully"}