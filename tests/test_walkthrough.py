import unittest
import os
from unittest.mock import patch, MagicMock
from src.walkthrough import WalkthroughWindow, check_first_launch

class TestWalkthrough(unittest.TestCase):
    @patch('src.walkthrough.QMainWindow')
    def test_walkthrough_window(self, mock_main_window):
        window = WalkthroughWindow()
        self.assertEqual(window.windowTitle(), "Initial Setup Walkthrough")
        self.assertEqual(window.current_step, 0)
        window.next_step()
        self.assertEqual(window.current_step, 1)

    @patch('os.path.exists')
    def test_check_first_launch(self, mock_exists):
        mock_exists.return_value = False
        self.assertTrue(check_first_launch())
        mock_exists.return_value = True
        self.assertFalse(check_first_launch())

if __name__ == '__main__':
    unittest.main()