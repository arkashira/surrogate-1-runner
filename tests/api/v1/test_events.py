import pytest
from flask import json
from src.api.v1.events import events_bp

@pytest.fixture
def client():
    from src.app import create_app
    app = create_app()
    app.register_blueprint(events_bp, url_prefix='/api/v1')
    client = app.test_client()
    yield client

def test_post_event_success(client):
    data = {
        'title': 'Test Event',
        'text': 'This is a test event',
        'tags': ['test', 'event'],
        'timestamp': '2023-05-05T12:00:00+00:00'
    }
    response = client.post('/api/v1/events', json=data)
    assert response.status_code == 202
    assert response.json['status'] == 'ok'
    assert 'event' in response.json

def test_post_event_missing_fields(client):
    data = {
        'title': 'Test Event',
        'text': 'This is a test event'
    }
    response = client.post('/api/v1/events', json=data)
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert 'errors' in response.json
    assert any('Title and Text are required and must be strings' in error['message'] for error in response.json['errors'])

def test_post_event_invalid_timestamp(client):
    data = {
        'title': 'Test Event',
        'text': 'This is a test event',
        'tags': ['test', 'event'],
        'timestamp': 'invalid-timestamp'
    }
    response = client.post('/api/v1/events', json=data)
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert 'errors' in response.json
    assert any('Invalid timestamp format' in error['message'] for error in response.json['errors'])

def test_post_event_invalid_body(client):
    data = "not a json"
    response = client.post('/api/v1/events', data=data, content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert 'errors' in response.json
    assert any('Request body must be a valid JSON object' in error['message'] for error in response.json['errors'])