import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from pathlib import Path
from audit_logger import AuditLogger

class TestAuditLogger(unittest.TestCase):
    def setUp(self):
        self.test_log_dir = Path("/tmp/test_audit_logs")
        self.test_log_dir.mkdir(parents=True, exist_ok=True)
        self.audit_logger = AuditLogger(log_dir=self.test_log_dir)

    def tearDown(self):
        for log_file in self.test_log_dir.glob("*.log"):
            log_file.unlink()
        self.test_log_dir.rmdir()

    @patch('audit_logger.logging.FileHandler')
    def test_log_request(self, mock_file_handler):
        mock_handler = MagicMock()
        mock_file_handler.return_value = mock_handler

        self.audit_logger.log_request("192.168.1.1", "Claude")

        mock_handler.write.assert_called_once()
        log_message = mock_handler.write.call_args[0][0]
        self.assertIn("IP Hash", log_message)
        self.assertIn("Service Type: Claude", log_message)

    def test_cleanup_old_logs(self):
        old_log = self.test_log_dir / "old.log"
        old_log.touch()
        old_log_time = datetime.now() - timedelta(days=91)
        old_log.utime((old_log_time.timestamp(), old_log_time.timestamp()))

        new_log = self.test_log_dir / "new.log"
        new_log.touch()

        self.audit_logger.cleanup_old_logs()

        self.assertFalse(old_log.exists())
        self.assertTrue(new_log.exists())

if __name__ == '__main__':
    unittest.main()