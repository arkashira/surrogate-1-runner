import pytest
from fastapi.testclient import TestClient
from src.metrics import app, bearer_token

client = TestClient(app)

def test_metrics_endpoint_without_token():
    response = client.get("/metrics")
    assert response.status_code == 401

def test_metrics_endpoint_with_invalid_token():
    response = client.get("/metrics", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401

def test_metrics_endpoint_with_valid_token():
    response = client.get("/metrics", headers={"Authorization": f"Bearer {bearer_token}"})
    assert response.status_code == 200
    assert b"surrogate_checks_total" in response.content

def test_check_endpoint():
    response = client.post("/check?service=test_service")
    assert response.status_code == 200
    assert response.json() == {"message": "Check recorded"}

def test_check_error_endpoint():
    response = client.post("/check_error?service=test_service")
    assert response.status_code == 200
    assert response.json() == {"message": "Check error recorded"}

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}