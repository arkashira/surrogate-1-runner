import unittest
from ui import UI
from transcription_settings import TranscriptionSettings
from config.config_schema import ConfigSchema

class TestUI(unittest.TestCase):
    def setUp(self):
        self.config = ConfigSchema()
        self.settings = TranscriptionSettings(self.config)
        self.ui = UI(self.settings)

    def test_render_audio_gain_control_status(self):
        self.ui.handle_toggle_audio_gain_control()
        self.assertIn("Microphone boost is active.", self.ui.render_audio_gain_control_status())

if __name__ == '__main__':
    unittest.main()