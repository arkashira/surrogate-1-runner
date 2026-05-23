import unittest
import numpy as np
from src.audio_processing import AudioProcessor

class TestAudioProcessor(unittest.TestCase):
    def setUp(self):
        self.audio_processor = AudioProcessor()
        self.test_audio_data = np.array([1.0, 2.0, 3.0, 4.0])

    def test_apply_gain_boost_disabled(self):
        result = self.audio_processor.apply_gain_boost(self.test_audio_data)
        np.testing.assert_array_equal(result, self.test_audio_data)

    def test_apply_gain_boost_enabled(self):
        self.audio_processor.toggle_gain_boost(True)
        result = self.audio_processor.apply_gain_boost(self.test_audio_data)
        expected_result = self.test_audio_data * self.audio_processor.gain_boost_factor
        np.testing.assert_array_equal(result, expected_result)

    def test_toggle_gain_boost(self):
        self.audio_processor.toggle_gain_boost(True)
        self.assertTrue(self.audio_processor.gain_boost_enabled)
        self.audio_processor.toggle_gain_boost(False)
        self.assertFalse(self.audio_processor.gain_boost_enabled)

    def test_set_gain_boost_factor(self):
        new_factor = 3.0
        self.audio_processor.set_gain_boost_factor(new_factor)
        self.assertEqual(self.audio_processor.gain_boost_factor, new_factor)

if __name__ == '__main__':
    unittest.main()