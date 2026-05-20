import unittest
from unittest.mock import patch
from ingest_worker import retry_with_exponential_backoff, download_dataset

class TestRetryWithExponentialBackoff(unittest.TestCase):

    @patch('ingest_worker.time.sleep')
    @patch('ingest_worker.logger')
    def test_retry_with_exponential_backoff(self, mock_logger, mock_sleep):
        mock_logger.error.side_effect = lambda msg: print(msg)
        
        @retry_with_exponential_backoff
        def failing_function():
            raise Exception("Test failure")

        with self.assertRaises(Exception):
            failing_function()

        expected_sleep_calls = [1, 2, 4, 8, 16]
        actual_sleep_calls = [call[0][0] for call in mock_sleep.call_args_list]

        self.assertEqual(actual_sleep_calls, expected_sleep_calls)

if __name__ == '__main__':
    unittest.main()