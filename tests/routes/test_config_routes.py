from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_update_config_valid():
    config_data = {
        'notification_preferences': {'email': True, 'sms': False},
        'health_check_interval': 30
    }
    response = client.post('/config', json=config_data)
    assert response.status_code == 200
    assert response.json() == {'message': 'Configuration updated successfully', 'config': config_data}

def test_update_config_invalid_health_check_interval():
    config_data = {
        'notification_preferences': {'email': True, 'sms': False},
        'health_check_interval': -1
    }
    response = client.post('/config', json=config_data)
    assert response.status_code == 400
    assert 'Health check interval must be a positive integer' in response.json()['detail']

def test_update_config_invalid_notification_preferences():
    config_data = {
        'notification_preferences': 'invalid',
        'health_check_interval': 30
    }
    response = client.post('/config', json=config_data)
    assert response.status_code == 400
    assert 'Notification preferences must be a dictionary' in response.json()['detail']