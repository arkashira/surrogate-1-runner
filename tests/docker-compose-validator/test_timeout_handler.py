import unittest
from unittest.mock import patch
from src.docker-compose-validator.timeout_handler import TimeoutHandler

class TestTimeoutHandler(unittest.TestCase):
    def test_check_health(self):
        with patch('subprocess.check_output') as mock_check_output:
            mock_check_output.return_value = b"PostgreSQL is healthy"
            timeout_handler = TimeoutHandler("test_container")
            self.assertTrue(timeout_handler.check_health())

    def test_check_health_failure(self):
        with patch('subprocess.check_output') as mock_check_output:
            mock_check_output.return_value = b"PostgreSQL failed to bind port 5432"
            timeout_handler = TimeoutHandler("test_container")
            self.assertFalse(timeout_handler.check_health())

    def test_validate_compose_success(self):
        with patch('src.docker-compose-validator.timeout_handler.TimeoutHandler.check_health') as mock_check_health:
            mock_check_health.return_value = True
            timeout_handler = TimeoutHandler("test_container")
            self.assertTrue(timeout_handler.validate_compose())

    def test_validate_compose_failure(self):
        with patch('src.docker-compose-validator.timeout_handler.TimeoutHandler.check_health') as mock_check_health:
            mock_check_health.return_value = False
            timeout_handler = TimeoutHandler("test_container")
            self.assertFalse(timeout_handler.validate_compose())

    def test_exit_compose(self):
        with patch('sys.exit') as mock_exit:
            timeout_handler = TimeoutHandler("test_container")
            timeout_handler.exit_compose(1)
            mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()