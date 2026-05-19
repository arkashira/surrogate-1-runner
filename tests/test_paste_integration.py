import unittest
from unittest.mock import patch
import time
import logging
from surrogate_1.paste import paste, PasteError
from surrogate_1.main import paste_data, paste_cascade_fixer

class TestPasteIntegration(unittest.TestCase):
    @patch('surrogate_1.paste.paste_cascade_fixer.PasteCascadeFixer')
    def test_paste_no_breaking_changes(self, mock_paste_cascade_fixer):
        mock_paste_cascade_fixer.return_value = object()
        paste("test data")

    @patch('surrogate_1.paste.paste_cascade_fixer.PasteCascadeFixer')
    def test_minimal_performance_overhead(self, mock_paste_cascade_fixer):
        mock_paste_cascade_fixer.return_value = object()
        start_time = time.time()
        paste("test data")
        elapsed_time = time.time() - start_time
        self.assertLess(elapsed_time, 0.005)

    @patch('surrogate_1.paste.paste_cascade_fixer.PasteCascadeFixer')
    def test_proper_error_handling(self, mock_paste_cascade_fixer):
        mock_paste_cascade_fixer.side_effect = PasteError("Test error")
        with self.assertRaises(PasteError):
            paste("test data with error")

    @patch('surrogate_1.paste.paste_cascade_fixer.PasteCascadeFixer')
    def test_logging(self, mock_paste_cascade_fixer):
        mock_paste_cascade_fixer.return_value = object()
        logging.basicConfig(level=logging.DEBUG)
        paste("test data")
        log_entries = logging.getLogger("").handlers[0].buffer.getvalue().splitlines()
        self.assertIn("Pasting test data", log_entries)

    def test_paste_with_fixer(self):
        input_data = "Line1\nLine2"
        expected_output = "Line1 Line2"
        result = paste_data(input_data)
        self.assertEqual(result, expected_output)

    def test_paste_performance(self):
        start = time.time()
        paste_data("Performance test")
        end = time.time()
        latency = (end - start) * 1000  # ms
        self.assertLess(latency, 5)

    def test_paste_error_handling(self):
        with self.assertLogs(level='ERROR') as log:
            paste_data(None)
        self.assertIn("Invalid input data", log.output[0])

if __name__ == '__main__':
    unittest.main()