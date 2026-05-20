import unittest
from src.root_cause_analysis import RootCauseAnalysis

class TestRootCauseAnalysis(unittest.TestCase):
    def setUp(self):
        self.root_cause_analyzer = RootCauseAnalysis()

    def test_analyze_incident(self):
        incident_id = "incident_123"
        incident_data = {"error": "System error"}
        report = self.root_cause_analyzer.analyze_incident(incident_id, incident_data)
        self.assertEqual(report["incident_id"], incident_id)
        self.assertEqual(report["root_cause"], "System error")
        self.assertIn("Check system logs for detailed error messages.", report["recommendations"])

    def test_get_incident_report(self):
        incident_id = "incident_123"
        incident_data = {"error": "System error"}
        self.root_cause_analyzer.analyze_incident(incident_id, incident_data)
        report = self.root_cause_analyzer.get_incident_report(incident_id)
        self.assertIsNotNone(report)
        self.assertEqual(report["incident_id"], incident_id)

if __name__ == "__main__":
    unittest.main()