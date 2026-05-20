import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming main.py is the entry point of your FastAPI application

client = TestClient(app)

def test_filter_tests_by_coverage():
    response = client.get("/api/v1/test-filter")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tests"]) > 0
    assert data["tests"][0]["coverage_impact"] in ["high", "medium", "low"]

def test_handle_webhook():
    response = client.post("/api/v1/test-filter/webhook", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["filtered_tests"]["tests"]) > 0