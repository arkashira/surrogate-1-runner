import unittest
from unittest.mock import patch, Mock
from orchestrator import RetryStrategy, orchestrate_llm_calls

class TestRetryStrategy(unittest.TestCase):
    def setUp(self):
        self.retry_strategy = RetryStrategy(max_retries=2, backoff_factor=0.1)

    @patch('time.sleep')
    def test_execute_with_retry_success(self, mock_sleep):
        mock_func = Mock(side_effect=[Exception("Retry"), "Success"])
        result = self.retry_strategy.execute_with_retry(mock_func)
        self.assertEqual(result, "Success")
        self.assertEqual(mock_func.call_count, 2)
        self.assertEqual(mock_sleep.call_count, 1)

    @patch('time.sleep')
    def test_execute_with_retry_failure(self, mock_sleep):
        mock_func = Mock(side_effect=[Exception("Retry"), Exception("Retry"), Exception("Final Failure")])
        with self.assertRaises(Exception):
            self.retry_strategy.execute_with_retry(mock_func)
        self.assertEqual(mock_func.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

class TestOrchestrateLLMCalls(unittest.TestCase):
    @patch('orchestrator.RetryStrategy')
    def test_orchestrate_llm_calls(self, mock_retry_strategy):
        mock_retry_strategy_instance = Mock()
        mock_retry_strategy.return_value = mock_retry_strategy_instance
        mock_retry_strategy_instance.execute_with_retry.return_value = "Success"
        
        result = orchestrate_llm_calls(Mock(), "arg1", kwarg1="value1")
        self.assertEqual(result, "Success")
        mock_retry_strategy.assert_called_once()
        mock_retry_strategy_instance.execute_with_retry.assert_called_once()

if __name__ == '__main__':
    unittest.main()