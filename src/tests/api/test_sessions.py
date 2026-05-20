import pytest
from fastapi.testclient import TestClient
from ...main import app

client = TestClient(app)

def test_list_sessions():
    response = client.get("/sessions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_session():
    # Assuming there's a session with id "test_session"
    response = client.delete("/sessions/test_session")
    assert response.status_code == 204

def test_delete_nonexistent_session():
    response = client.delete("/sessions/nonexistent")
    assert response.status_code == 404