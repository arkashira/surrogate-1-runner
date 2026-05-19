
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.api.policy import app, policies

def setup_module(module):
    global policies
    policies = {}

def teardown_module(module):
    global policies
    policies.clear()

def test_read_policy():
    policies["policy1"] = '{"rule": "always_approve"}'
    client = TestClient(app)
    response = client.get("/policy/policy1")
    assert response.status_code == 200
    assert response.json() == {'content': '{"rule": "always_approve"}'}

def test_create_policy():
    client = TestClient(app)
    response = client.post("/policy", json={'id': 'policy1', 'content': '{"rule": "always_approve"}'})
    assert response.status_code == 200
    assert response.json() == {'message': 'Policy created'}
    assert "policy1" in policies

def test_read_non_existent_policy():
    client = TestClient(app)
    response = client.get("/policy/non_existent_policy")
    assert response.status_code == 404