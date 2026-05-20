import unittest
from unittest.mock import patch, MagicMock
from src.onboarding.api_key_validator import APIKeyValidator

class TestAPIKeyValidator(unittest.TestCase):
    @patch('requests.get')
    def test_validate_success(self, mock_get):
        mock_get.return_value.status_code = 200
        validator = APIKeyValidator('valid_api_key')
        self.assertTrue(validator.validate())

    @patch('requests.get')
    def test_validate_failure(self, mock_get):
        mock_get.return_value.status_code = 401
        validator = APIKeyValidator('invalid_api_key')
        self.assertFalse(validator.validate())

    @patch('requests.get')
    def test_validate_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException
        validator = APIKeyValidator('valid_api_key')
        self.assertFalse(validator.validate())

    @patch('requests.get')
    def test_static_validate_api_key(self, mock_get):
        """Test the static convenience method."""
        mock_get.return_value.status_code = 200
        result = APIKeyValidator.validate_api_key('test_key')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()