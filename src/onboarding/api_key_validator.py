import requests
from typing import Optional

class APIKeyValidator:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def validate(self) -> bool:
        """Validate the API key by making a test request to the API."""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.get('https://api.example.com/validate', headers=headers)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Static method to validate an API key (convenience wrapper)."""
        validator = APIKeyValidator(api_key)
        return validator.validate()