import unittest
from transcription_accuracy_analyzer import TranscriptionAccuracyAnalyzer

class TestTranscriptionAccuracyAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = TranscriptionAccuracyAnalyzer()
        self.audio_file_path = "test_audio.wav"
        self.reference_transcript = "This is a test transcript."

    def test_analyze_accuracy(self):
        accuracy = self.analyzer.analyze_accuracy(self.audio_file_path, self.reference_transcript)
        self.assertIsInstance(accuracy, float)
        self.assertGreaterEqual(accuracy, 0.15)  # Ensure accuracy is at least 15%

if __name__ == '__main__':
    unittest.main()