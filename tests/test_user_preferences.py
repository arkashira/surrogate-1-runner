import unittest
from src.user_preferences import UserPreferences

class TestUserPreferences(unittest.TestCase):
    def setUp(self):
        self.preferences = UserPreferences()

    def test_set_brightness(self):
        self.preferences.set_brightness(0.5)
        self.assertEqual(self.preferences.preferences['brightness'], 0.5)
        self.assertFalse(self.preferences.preferences['auto_adjust'])

    def test_get_preferences(self):
        preferences = self.preferences.get_preferences()
        self.assertEqual(preferences['brightness'], 1.0)
        self.assertTrue(preferences['auto_adjust'])

if __name__ == '__main__':
    unittest.main()