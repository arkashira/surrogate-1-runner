"""
Test that the `/metrics` endpoint is reachable and returns a valid
Prometheus metrics payload.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    # Basic sanity check: response should contain the Prometheus
    # content type header and some metric text.
    assert response.headers["content-type"] == "text/plain; version=0.0.4; charset=utf-8"
    assert b"# HELP" in response.content or b"# TYPE" in response.content