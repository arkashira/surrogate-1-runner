import unittest
from unittest.mock import patch, MagicMock
import time
from src.retry import retry_with_backoff

class TestRetryMechanism(unittest.TestCase):

    def test_successful_call_no_retries(self):
        """Test that a successful function call doesn't trigger retries"""
        mock_func = MagicMock(return_value="success")
        
        result = retry_with_backoff(mock_func, max_retries=3, base_delay=0.1)
        
        self.assertEqual(result, "success")
        mock_func.assert_called_once()

    @patch('time.sleep')
    def test_retry_on_failure_then_success(self, mock_sleep):
        """Test that function is retried on failure then succeeds"""
        mock_func = MagicMock(side_effect=[Exception("Failed"), "success"])
        
        result = retry_with_backoff(mock_func, max_retries=3, base_delay=0.1)
        
        self.assertEqual(result, "success")
        self.assertEqual(mock_func.call_count, 2)
        mock_sleep.assert_called_once_with(0.1)

    @patch('time.sleep')
    def test_retry_exhausted(self, mock_sleep):
        """Test that function stops retrying after max retries"""
        mock_func = MagicMock(side_effect=Exception("Failed"))
        
        with self.assertRaises(Exception) as context:
            retry_with_backoff(mock_func, max_retries=2, base_delay=0.1)
        
        self.assertEqual(mock_func.call_count, 3)  # initial + 2 retries
        self.assertIn("Failed", str(context.exception))

    @patch('time.sleep')
    def test_exponential_backoff(self, mock_sleep):
        """Test that delays increase exponentially"""
        mock_func = MagicMock(side_effect=[Exception("Failed"), Exception("Failed"), "success"])
        
        retry_with_backoff(mock_func, max_retries=3, base_delay=0.1)
        
        expected_delays = [0.1, 0.2]  # 0.1 * 2^0, 0.1 * 2^1
        mock_sleep.assert_has_calls([unittest.mock.call(delay) for delay in expected_delays])

    @patch('logging.Logger.error')
    def test_logging_on_retry(self, mock_log_error):
        """Test that retries are logged with error details"""
        mock_func = MagicMock(side_effect=[Exception("Network error"), "success"])
        
        retry_with_backoff(mock_func, max_retries=2, base_delay=0.1)
        
        # Check that error was logged for the first failure
        mock_log_error.assert_called_with(
            "Retry attempt 1 failed: Network error",
            exc_info=True
        )

if __name__ == '__main__':
    unittest.main()