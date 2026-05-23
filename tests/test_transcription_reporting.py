import unittest
import pandas as pd
from transcription_reporting import TranscriptionReporting

class TestTranscriptionReporting(unittest.TestCase):
    def setUp(self):
        self.reporting = TranscriptionReporting()
        self.audio_files = ["test_audio1.wav", "test_audio2.wav"]
        self.reference_transcripts = ["This is a test transcript.", "Another test transcript."]

    def test_generate_report(self):
        report = self.reporting.generate_report(self.audio_files, self.reference_transcripts)
        self.assertIsInstance(report, pd.DataFrame)
        self.assertEqual(len(report), len(self.audio_files))

    def test_save_report(self):
        report = self.reporting.generate_report(self.audio_files, self.reference_transcripts)
        self.reporting.save_report(report, "test_report.csv")
        saved_report = pd.read_csv("test_report.csv")
        self.assertEqual(len(saved_report), len(self.audio_files))

if __name__ == '__main__':
    unittest.main()