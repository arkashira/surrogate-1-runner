import pytest
from fastapi.testclient import TestClient
from src.web.api.main import app

client = TestClient(app)

def test_get_templates():
    response = client.get("/api/templates")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 5  # Ensure at least 5 templates are listed