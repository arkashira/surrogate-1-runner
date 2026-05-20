import pytest
from src.validators.config_validator import validate_config

def test_validate_config_valid():
    config_data = {
        'notification_preferences': {'email': True, 'sms': False},
        'health_check_interval': 30
    }
    validated_config = validate_config(config_data)
    assert validated_config == config_data

def test_validate_config_invalid_health_check_interval():
    config_data = {
        'notification_preferences': {'email': True, 'sms': False},
        'health_check_interval': -1
    }
    with pytest.raises(ValueError, match='Health check interval must be a positive integer'):
        validate_config(config_data)

def test_validate_config_invalid_notification_preferences():
    config_data = {
        'notification_preferences': 'invalid',
        'health_check_interval': 30
    }
    with pytest.raises(ValueError, match='Notification preferences must be a dictionary'):
        validate_config(config_data)