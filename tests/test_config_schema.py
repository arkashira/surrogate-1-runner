import unittest
from config.config_schema import ConfigSchema

class TestConfigSchema(unittest.TestCase):
    def test_default_values(self):
        config = ConfigSchema()
        self.assertFalse(config.audio_gain_control_enabled)
        self.assertEqual(config.audio_gain_boost_level, 1.0)

    def test_custom_values(self):
        config = ConfigSchema(audio_gain_control_enabled=True, audio_gain_boost_level=1.5)
        self.assertTrue(config.audio_gain_control_enabled)
        self.assertEqual(config.audio_gain_boost_level, 1.5)

if __name__ == '__main__':
    unittest.main()