import unittest
from audio_guard.gain_normalizer import GainNormalizer
from pydub import AudioSegment

class TestGainNormalizer(unittest.TestCase):
    def setUp(self):
        self.normalizer = GainNormalizer()

    def test_normalize_audio(self):
        audio = AudioSegment.from_file("test_input.wav")
        normalized_audio = self.normalizer.normalize_audio(audio)
        dbfs = normalized_audio.dBFS
        self.assertTrue(-8 <= dbfs <= -4, "Normalized audio level is not within expected range")

if __name__ == '__main__':
    unittest.main()