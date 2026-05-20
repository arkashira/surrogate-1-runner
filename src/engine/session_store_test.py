import unittest
from datetime import datetime
from session_store import SessionStore

class TestSessionStore(unittest.TestCase):
    def setUp(self):
        self.store = SessionStore()
        self.store.add_native_speaker("speaker1")
        self.store.add_native_speaker("speaker2")

    def test_create_session(self):
        session_id = self.store.create_session("user1", "speaker1")
        self.assertIsNotNone(session_id)
        session = self.store.get_session(session_id)
        self.assertEqual(session["user_id"], "user1")
        self.assertEqual(session["native_speaker_id"], "speaker1")
        self.assertEqual(session["status"], "active")

    def test_unavailable_speaker(self):
        self.store.create_session("user1", "speaker1")
        with self.assertRaises(ValueError):
            self.store.create_session("user2", "speaker1")

    def test_end_session(self):
        session_id = self.store.create_session("user1", "speaker1")
        self.assertTrue(self.store.end_session(session_id))
        session = self.store.get_session(session_id)
        self.assertEqual(session["status"], "completed")
        self.assertTrue(self.store.native_speakers["speaker1"])

    def test_get_available_speakers(self):
        available = self.store.get_available_native_speakers()
        self.assertIn("speaker1", available)
        self.assertIn("speaker2", available)
        self.store.create_session("user1", "speaker1")
        available = self.store.get_available_native_speakers()
        self.assertNotIn("speaker1", available)
        self.assertIn("speaker2", available)

    def test_get_user_sessions(self):
        session_id1 = self.store.create_session("user1", "speaker1")
        session_id2 = self.store.create_session("user2", "speaker2")
        user1_sessions = self.store.get_user_sessions("user1")
        self.assertEqual(len(user1_sessions), 1)
        self.assertEqual(user1_sessions[0]["session_id"], session_id1)

    def test_log_session_data(self):
        session_id = self.store.create_session("user1", "speaker1")
        self.store.log_session_data(session_id, "http://example.com/recording.mp4")
        session = self.store.get_session(session_id)
        self.assertEqual(session["recording_url"], "http://example.com/recording.mp4")

if __name__ == "__main__":
    unittest.main()