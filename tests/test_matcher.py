import unittest
from src.engine.matcher import Matcher

class TestMatcher(unittest.TestCase):
    def setUp(self):
        self.native_speakers = ["Alice", "Bob", "Charlie"]
        self.matcher = Matcher(self.native_speakers)

    def test_find_match_returns_native_speaker(self):
        matched_speaker = self.matcher.find_match()
        self.assertIn(matched_speaker, self.native_speakers)

    def test_find_match_returns_none_if_no_speakers_available(self):
        self.matcher.native_speakers = []
        matched_speaker = self.matcher.find_match()
        self.assertIsNone(matched_speaker)

if __name__ == "__main__":
    unittest.main()