import unittest
import numpy as np
from whisper_wrapper import WhisperWrapper

class TestWhisperWrapper(unittest.TestCase):
    def setUp(self):
        self.whisper_wrapper = WhisperWrapper(model_name="tiny", device="cpu")

    def test_transcribe_stream(self):
        # Create a dummy audio frame
        audio_frames = np.random.randint(-32768, 32767, 16000, dtype=np.int16)

        # Test the transcribe_stream method
        result = self.whisper_wrapper.transcribe_stream(audio_frames)

        # Check if the result contains the required fields
        self.assertIn("text", result)
        self.assertIn("confidence", result)

        # Check if the confidence is a float between 0 and 1
        self.assertIsInstance(result["confidence"], float)
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)

if __name__ == "__main__":
    unittest.main()