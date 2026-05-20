import unittest
import time
from unittest.mock import patch
from session_monitor import SessionMonitor

class TestSessionMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = SessionMonitor()

    def test_start_session(self):
        self.monitor.start_session("session1")
        self.assertIn("session1", self.monitor.active_sessions)

    def test_end_session(self):
        self.monitor.start_session("session1")
        self.monitor.end_session("session1")
        self.assertNotIn("session1", self.monitor.active_sessions)

    def test_record_disconnection(self):
        self.monitor.record_disconnection("session1")
        self.assertEqual(self.monitor.session_disconnections["session1"], 1)

    def test_get_active_sessions(self):
        self.monitor.start_session("session1")
        self.monitor.start_session("session2")
        self.assertEqual(set(self.monitor.get_active_sessions()), {"session1", "session2"})

    def test_get_disconnection_stats(self):
        self.monitor.record_disconnection("session1")
        self.monitor.record_disconnection("session1")
        self.monitor.record_disconnection("session2")
        self.assertEqual(self.monitor.get_disconnection_stats(), {"session1": 2, "session2": 1})

if __name__ == "__main__":
    unittest.main()