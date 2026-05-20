import unittest
from battery_guard.health import get_battery_health_score

class TestHealth(unittest.TestCase):
    def test_score_range(self):
        score = get_battery_health_score()
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

if __name__ == "__main__":
    unittest.main()