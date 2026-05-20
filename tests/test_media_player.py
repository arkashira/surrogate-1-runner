import unittest
import cv2
import numpy as np
from src.media_player import MediaPlayer

class TestMediaPlayer(unittest.TestCase):
    def setUp(self):
        self.player = MediaPlayer()

    def test_set_brightness(self):
        self.player.set_brightness(0.5)
        self.assertEqual(self.player.brightness, 0.5)
        self.assertFalse(self.player.auto_adjust)

    def test_auto_adjust_brightness(self):
        # Create a test frame with low brightness
        low_brightness_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        adjusted_frame = self.player.auto_adjust_brightness(low_brightness_frame)
        self.assertEqual(self.player.brightness, 1.5)

        # Create a test frame with medium brightness
        medium_brightness_frame = np.ones((100, 100, 3), dtype=np.uint8) * 128
        adjusted_frame = self.player.auto_adjust_brightness(medium_brightness_frame)
        self.assertEqual(self.player.brightness, 1.2)

        # Create a test frame with high brightness
        high_brightness_frame = np.ones((100, 100, 3), dtype=np.uint8) * 255
        adjusted_frame = self.player.auto_adjust_brightness(high_brightness_frame)
        self.assertEqual(self.player.brightness, 1.0)

    def test_play(self):
        # This test is more of an integration test and might require a test video file
        pass

if __name__ == '__main__':
    unittest.main()