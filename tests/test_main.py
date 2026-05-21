import pytest
from fastapi.testclient import TestClient
from src.main import app, AIRequest

client = TestClient(app)

def test_ai_endpoint_with_valid_model():
    payload = AIRequest(model="gpt-4", messages=[{"role": "user", "content": "Hello"}])
    response = client.post("/ai", json=payload.dict())
    assert response.status_code == 200

def test_ai_endpoint_with_invalid_model():
    payload = AIRequest(model="invalid-model", messages=[{"role": "user", "content": "Hello"}])
    response = client.post("/ai", json=payload.dict())
    assert response.status_code == 400

def test_ai_endpoint_with_missing_model():
    payload = AIRequest(messages=[{"role": "user", "content": "Hello"}])
    response = client.post("/ai", json=payload.dict())
    assert response.status_code == 422  # Unprocessable Entity (422) for validation error

def test_ai_endpoint_with_invalid_payload():
    payload = {"invalid_key": "invalid_value"}
    response = client.post("/ai", json=payload)
    assert response.status_code == 422  # Unprocessable Entity (422) for validation error