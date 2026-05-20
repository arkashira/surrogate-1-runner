import pytest
from fastapi.testclient import TestClient
from surrogate_1.api.alerts import router

client = TestClient(router)

def test_get_latest_alert_valid_token():
    response = client.get("/api/alerts/latest", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200

def test_get_latest_alert_invalid_token():
    response = client.get("/api/alerts/latest", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401

def test_get_latest_alert_no_alerts():
    # Assume no alerts in the database
    response = client.get("/api/alerts/latest", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert response.json() == {"id": 0, "message": "No alerts found"}

def test_get_latest_alert_with_alerts():
    # Assume an alert in the database
    response = client.get("/api/alerts/latest", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert response.json()["id"] > 0
    assert response.json()["message"] != ""