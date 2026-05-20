import unittest
from transcription_settings import TranscriptionSettings
from config.config_schema import ConfigSchema

class TestTranscriptionSettings(unittest.TestCase):
    def setUp(self):
        self.config = ConfigSchema()
        self.settings = TranscriptionSettings(self.config)

    def test_toggle_audio_gain_control(self):
        self.settings.toggle_audio_gain_control(True)
        self.assertTrue(self.settings.config.audio_gain_control_enabled)
        self.settings.toggle_audio_gain_control(False)
        self.assertFalse(self.settings.config.audio_gain_control_enabled)

    def test_apply_audio_gain_boost(self):
        self.settings.config.audio_gain_boost_level = 2.0
        self.settings.config.audio_gain_control_enabled = True
        boosted_audio = self.settings.apply_audio_gain_boost(1.0)
        self.assertEqual(boosted_audio, 2.0)

if __name__ == '__main__':
    unittest.main()