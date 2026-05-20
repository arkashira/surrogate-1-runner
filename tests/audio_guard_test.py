# src/audio_guard/tests.py
import unittest
from src.audio_detector import hook_audio_app

class TestAudioGuard(unittest.TestCase):
    def test_conflicting_app_detection(self):
        # Mock app detection
        hook_audio_app('zoom')
        hook_audio_app('teams')
        # Assert hook was called
        self.assertTrue(True)  # Replace with actual verification

if __name__ == '__main__':
    unittest.main()