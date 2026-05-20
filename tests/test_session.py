import pytest
from fastapi.testclient import TestClient
from src.backend.api.main import app

client = TestClient(app)

def test_start_session():
    response = client.post("/session/start", headers={"Authorization": "Bearer your_token_here"})
    assert response.status_code == 200
    assert response.json() == {"message": "Session started"}

def test_start_session_without_permission():
    response = client.post("/session/start", headers={"Authorization": "Bearer your_token_here"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

def test_start_session_with_invalid_token():
    response = client.post("/session/start", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}