import unittest
from unittest.mock import MagicMock
from src.retry_strategy import RetryStrategy

class TestRetryStrategy(unittest.TestCase):
    def test_successful_execution(self):
        mock_func = MagicMock(return_value="success")
        retry_strategy = RetryStrategy(max_retries=3)
        result = retry_strategy.execute_with_retry(mock_func)
        self.assertEqual(result, "success")
        mock_func.assert_called_once()

    def test_retry_on_failure(self):
        mock_func = MagicMock(side_effect=[Exception("fail"), Exception("fail"), "success"])
        retry_strategy = RetryStrategy(max_retries=3)
        result = retry_strategy.execute_with_retry(mock_func)
        self.assertEqual(result, "success")
        self.assertEqual(mock_func.call_count, 3)

    def test_max_retries_exceeded(self):
        mock_func = MagicMock(side_effect=Exception("fail"))
        retry_strategy = RetryStrategy(max_retries=3)
        with self.assertRaises(Exception) as context:
            retry_strategy.execute_with_retry(mock_func)
        self.assertEqual(str(context.exception), "fail")
        self.assertEqual(mock_func.call_count, 4)

if __name__ == '__main__':
    unittest.main()