import pytest
from fastapi.testclient import TestClient
from ..api.main import app

client = TestClient(app)

def test_update_scoring_config_success():
    response = client.put(
        "/api/v1/scoring/config",
        json={"policy_severity": 0.6, "code_change_frequency": 0.4}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Scoring weights updated successfully"}

def test_update_scoring_config_invalid_weights():
    response = client.put(
        "/api/v1/scoring/config",
        json={"policy_severity": 0.7, "code_change_frequency": 0.3}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Weights must sum to 1.0"}