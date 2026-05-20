import pytest
from flask import Flask, jsonify
from surrogate_1.api.auth_middleware import authentication_middleware
from surrogate_1_sdk import API_KEY_HEADER

@pytest.fixture
def app():
    app = Flask(__name__)
    
    @app.route('/api/v1/data')
    @authentication_middleware
    def protected_endpoint():
        return jsonify({"data": "success"}), 200
    
    return app

def test_v09_backward_compatibility(app):
    """Critical: Ensure v0.9.x clients work without API keys"""
    client = app.test_client()
    response = client.get('/api/v1/data', headers={'X-API-Version': '0.9'})
    assert response.status_code == 200

def test_valid_api_key_accepted(app):
    client = app.test_client()
    response = client.get('/api/v1/data', headers={API_KEY_HEADER: 'valid-test-key'})
    assert response.status_code == 200
    assert response.json['data'] == 'success'

def test_missing_api_key_rejected(app):
    client = app.test_client()
    response = client.get('/api/v1/data')
    assert response.status_code == 401
    assert "Authentication required" in response.json['error']

def test_invalid_api_key_rejected(app):
    client = app.test_client()
    response = client.get('/api/v1/data', headers={API_KEY_HEADER: 'invalid-key'})
    assert response.status_code == 401
    assert "Invalid API key" in response.json['error']

def test_v10_requires_auth(app):
    """Ensure v1.0+ clients cannot bypass auth"""
    client = app.test_client()
    response = client.get('/api/v1/data', headers={'X-API-Version': '1.0'})
    assert response.status_code == 401