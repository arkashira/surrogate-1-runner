import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_decide_success():
    """Test successful decision invocation."""
    response = client.post(
        "/decide",
        json={"data": {"user_id": "test123", "action": "purchase", "amount": 99.99}}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "decision" in result
    assert "confidence" in result
    assert isinstance(result["decision"], str)
    assert 0 <= result["confidence"] <= 1

def test_decide_with_high_risk():
    """Test decision with high risk score."""
    response = client.post(
        "/decide",
        json={"data": {"user_id": "test456", "action": "purchase", "amount": 999.99, "risk_score": 0.9}}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["decision"] == "reject"

def test_decide_with_low_risk():
    """Test decision with low risk score."""
    response = client.post(
        "/decide",
        json={"data": {"user_id": "test789", "action": "purchase", "amount": 10.00, "risk_score": 0.1}}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["decision"] == "approve"

def test_decide_empty_context():
    """Test decision with empty context."""
    response = client.post(
        "/decide",
        json={"data": {}}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "decision" in result
    assert "confidence" in result