import unittest
from log_filtering import filter_logs

class TestLogFiltering(unittest.TestCase):
    def setUp(self):
        self.logs = [
            {'level': 'INFO', 'timestamp': '2023-05-01 12:00:00', 'message': 'Test message 1'},
            {'level': 'WARNING', 'timestamp': '2023-05-01 13:00:00', 'message': 'Test message 2'},
            {'level': 'ERROR', 'timestamp': '2023-05-01 14:00:00', 'message': 'Test message 3'}
        ]

    def test_filter_by_log_level(self):
        filtered_logs = filter_logs(self.logs, log_level='WARNING')
        self.assertEqual(len(filtered_logs), 1)
        self.assertEqual(filtered_logs[0]['level'], 'WARNING')

    def test_filter_by_timestamp(self):
        start_time = datetime.strptime('2023-05-01 12:30:00', '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime('2023-05-01 13:30:00', '%Y-%m-%d %H:%M:%S')
        filtered_logs = filter_logs(self.logs, start_time=start_time, end_time=end_time)
        self.assertEqual(len(filtered_logs), 1)
        self.assertEqual(filtered_logs[0]['timestamp'], '2023-05-01 13:00:00')


if __name__ == '__main__':
    unittest.main()