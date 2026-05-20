import unittest
from datetime import datetime, timedelta
from src.session_manager import SessionManager

class TestSessionManager(unittest.TestCase):
    def setUp(self):
        self.session_manager = SessionManager(timeout_minutes=1)

    def test_add_session(self):
        self.session_manager.add_session('session1', 'user1', 'node1')
        self.assertIn('session1', self.session_manager.sessions)

    def test_update_activity(self):
        self.session_manager.add_session('session1', 'user1', 'node1')
        old_activity = self.session_manager.sessions['session1']['last_activity']
        self.session_manager.update_activity('session1')
        new_activity = self.session_manager.sessions['session1']['last_activity']
        self.assertNotEqual(old_activity, new_activity)

    def test_get_active_sessions(self):
        self.session_manager.add_session('session1', 'user1', 'node1')
        active_sessions = self.session_manager.get_active_sessions()
        self.assertIn('session1', active_sessions)

        # Simulate timeout
        self.session_manager.sessions['session1']['last_activity'] = datetime.now() - timedelta(minutes=2)
        active_sessions = self.session_manager.get_active_sessions()
        self.assertNotIn('session1', active_sessions)
        self.assertEqual(self.session_manager.sessions['session1']['status'], 'timed_out')

    def test_terminate_session(self):
        self.session_manager.add_session('session1', 'user1', 'node1')
        self.assertTrue(self.session_manager.terminate_session('session1'))
        self.assertEqual(self.session_manager.sessions['session1']['status'], 'terminated')

    def test_get_session(self):
        self.session_manager.add_session('session1', 'user1', 'node1')
        session = self.session_manager.get_session('session1')
        self.assertIsNotNone(session)
        self.assertEqual(session['user'], 'user1')

if __name__ == '__main__':
    unittest.main()