import pytest
from fastapi.testclient import TestClient
from src.integration_api import app

client = TestClient(app)

def test_integrate_success():
    response = client.post(
        "/integrate",
        json={
            "organization_id": "test_org",
            "api_key": "test_key",
            "custom_settings": {"setting1": "value1"}
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Integration successful", "organization_id": "test_org"}

def test_integrate_missing_fields():
    response = client.post(
        "/integrate",
        json={
            "organization_id": "",
            "api_key": ""
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Organization ID and API key are required"}

def test_get_integration_success():
    # Assuming we have a way to mock the retrieval of integration config
    response = client.get("/integration/test_org")
    assert response.status_code == 200
    assert response.json() == {"organization_id": "test_org", "api_key": "test_key", "custom_settings": {"setting1": "value1"}}

def test_get_integration_not_found():
    response = client.get("/integration/nonexistent_org")
    assert response.status_code == 404
    assert response.json() == {"detail": "Integration not found"}