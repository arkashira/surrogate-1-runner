import unittest
from unittest.mock import patch, MagicMock
from logger import AuditLogger
from datetime import datetime

class TestAuditLogger(unittest.TestCase):
    @patch('psycopg2.connect')
    def setUp(self, mock_connect):
        self.mock_conn = MagicMock()
        mock_connect.return_value = self.mock_conn
        self.db_config = {
            'dbname': 'test_db',
            'user': 'test_user',
            'password': 'test_password',
            'host': 'localhost'
        }
        self.logger = AuditLogger(self.db_config)

    def test_log_download(self):
        video_metadata = {
            'title': 'Test Video',
            'id': '12345',
            'author': 'Test Author',
            'duration': '00:01:30'
        }
        self.logger.log_download('192.168.1.1', video_metadata)

        cursor = self.mock_conn.cursor.return_value.__enter__.return_value
        cursor.execute.assert_called_once_with(
            """
            INSERT INTO audit_logs (ip_address, download_time, video_title, video_id, video_author, video_duration)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            ('192.168.1.1', datetime.utcnow(), 'Test Video', '12345', 'Test Author', '00:01:30')
        )
        self.mock_conn.commit.assert_called_once()

    @patch('psycopg2.connect')
    def tearDown(self, mock_connect):
        self.logger.close()
        mock_connect.assert_called_once_with(**self.db_config)

if __name__ == '__main__':
    unittest.main()