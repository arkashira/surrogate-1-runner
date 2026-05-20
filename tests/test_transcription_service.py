import unittest
from transcription_service import TranscriptionService

class TestTranscriptionService(unittest.TestCase):
    def setUp(self):
        self.transcription_service = TranscriptionService("test_conversation.wav")
        self.test_text = "Hello, how are you?"

    def test_transcribe_audio(self):
        transcription = self.transcription_service.transcribe_audio()
        self.assertEqual(transcription, self.test_text)

    def test_save_transcription(self):
        transcription = self.test_text
        filename = self.transcription_service.save_transcription(transcription)
        with open(filename, 'r') as file:
            saved_text = file.read()
        self.assertEqual(saved_text, transcription)

if __name__ == '__main__':
    unittest.main()