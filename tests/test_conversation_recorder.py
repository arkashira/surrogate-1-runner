import unittest
from conversation_recorder import ConversationRecorder

class TestConversationRecorder(unittest.TestCase):
    def setUp(self):
        self.recorder = ConversationRecorder()

    def test_start_stop_recording(self):
        # This test will need manual verification since it involves audio recording
        self.recorder.start_recording()
        self.recorder.stop_recording()
        self.assertTrue(os.path.exists(self.recorder.get_filename()))

if __name__ == '__main__':
    unittest.main()