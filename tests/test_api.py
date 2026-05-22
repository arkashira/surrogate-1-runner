import pytest
from src.api.monitoring import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_performance(client):
    response = client.get("/performance")
    assert response.status_code == 200
    assert response.json()["cpu_usage"] == 0.5
    assert response.json()["memory_usage"] == 0.7
    assert response.json()["response_time"] == 100

def test_metrics(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.json()["cpu_usage"] == {"cpu_usage": "Counter", "description": "CPU usage metric"}