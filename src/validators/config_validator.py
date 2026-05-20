from typing import Dict, Any
from pydantic import BaseModel, ValidationError, validator

class ConfigValidator(BaseModel):
    notification_preferences: Dict[str, Any]
    health_check_interval: int

    @validator('health_check_interval')
    def validate_health_check_interval(cls, value):
        if value <= 0:
            raise ValueError('Health check interval must be a positive integer')
        return value

    @validator('notification_preferences')
    def validate_notification_preferences(cls, value):
        if not isinstance(value, dict):
            raise ValueError('Notification preferences must be a dictionary')
        return value

def validate_config(config_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        config = ConfigValidator(**config_data)
        return config.dict()
    except ValidationError as e:
        raise ValueError(f'Invalid configuration: {e}')