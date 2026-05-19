import unittest
from scoring_engine import ScoringEngine

class TestScoringEngine(unittest.TestCase):
    def test_critical_severity(self):
        self.assertEqual(ScoringEngine.calculate_audit_score('critical', 0), 60)
        self.assertEqual(ScoringEngine.calculate_audit_score('critical', 100), 100)
        self.assertEqual(ScoringEngine.calculate_audit_score('critical', 200), 100)

    def test_medium_severity(self):
        self.assertEqual(ScoringEngine.calculate_audit_score('medium', 0), 24)
        self.assertEqual(ScoringEngine.calculate_audit_score('medium', 90), 40 + round(90 * 0.4))

    def test_invalid_severity(self):
        self.assertEqual(ScoringEngine.calculate_audit_score('unknown', 50), 20 * 0.6 + 50 * 0.4)

    def test_boundaries(self):
        self.assertEqual(ScoringEngine.calculate_audit_score('low', 0), 1)
        self.assertEqual(ScoringEngine.calculate_audit_score('critical', 250), 100)

if __name__ == '__main__':
    unittest.main()