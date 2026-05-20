import unittest
from unittest.mock import patch, Mock
from orchestration_engine.retry_handler import RetryHandler

class TestRetryHandler(unittest.TestCase):
    def setUp(self):
        self.retry_handler = RetryHandler(max_retries=2, backoff_factor=0.1)

    @patch('requests.get')
    def test_handle_retry_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        response = self.retry_handler.handle_retry(requests.get, 'http://example.com')
        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_handle_retry_transient_error(self, mock_get):
        mock_response_500 = Mock()
        mock_response_500.status_code = 500
        mock_response_200 = Mock()
        mock_response_200.status_code = 200
        mock_get.side_effect = [mock_response_500, mock_response_200]
        response = self.retry_handler.handle_retry(requests.get, 'http://example.com')
        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_handle_retry_max_retries_exceeded(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        with self.assertRaises(Exception) as context:
            self.retry_handler.handle_retry(requests.get, 'http://example.com')
        self.assertTrue('Max retries exceeded' in str(context.exception))

if __name__ == '__main__':
    unittest.main()