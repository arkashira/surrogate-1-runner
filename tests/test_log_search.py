import unittest
from log_search import search_logs

class TestLogSearch(unittest.TestCase):
    def setUp(self):
        self.logs = [
            {'level': 'INFO', 'timestamp': '2023-05-01 12:00:00', 'message': 'Test message 1'},
            {'level': 'WARNING', 'timestamp': '2023-05-01 13:00:00', 'message': 'Test message 2'},
            {'level': 'ERROR', 'timestamp': '2023-05-01 14:00:00', 'message': 'Test message 3'}
        ]

    def test_search_by_keyword(self):
        searched_logs = search_logs(self.logs, keyword='message 2')
        self.assertEqual(len(searched_logs), 1)
        self.assertEqual(searched_logs[0]['message'], 'Test message 2')


if __name__ == '__main__':
    unittest.main()