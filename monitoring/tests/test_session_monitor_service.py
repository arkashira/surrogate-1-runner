import unittest
from unittest.mock import patch
from session_monitor_service import SessionMonitorService

class TestSessionMonitorService(unittest.TestCase):
    def setUp(self):
        self.service = SessionMonitorService()

    def test_handle_session_start(self):
        with patch.object(self.service.monitor, 'start_session') as mock_start:
            self.service.handle_session_start("session1")
            mock_start.assert_called_once_with("session1")

    def test_handle_session_end(self):
        with patch.object(self.service.monitor, 'end_session') as mock_end:
            self.service.handle_session_end("session1")
            mock_end.assert_called_once_with("session1")

    def test_handle_disconnection(self):
        with patch.object(self.service.monitor, 'record_disconnection') as mock_record:
            self.service.handle_disconnection("session1")
            mock_record.assert_called_once_with("session1")

    def test_get_active_sessions(self):
        with patch.object(self.service.monitor, 'get_active_sessions', return_value=["session1", "session2"]):
            self.assertEqual(self.service.get_active_sessions(), ["session1", "session2"])

    def test_get_disconnection_stats(self):
        with patch.object(self.service.monitor, 'get_disconnection_stats', return_value={"session1": 2, "session2": 1}):
            self.assertEqual(self.service.get_disconnection_stats(), {"session1": 2, "session2": 1})

if __name__ == "__main__":
    unittest.main()