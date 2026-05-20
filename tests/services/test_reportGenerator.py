import unittest
from src.services.reportGenerator import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.sample_events = [
            {'timestamp': 1623456789, 'description': 'Event 1 occurred'},
            {'timestamp': 1623456800, 'description': 'Event 2 occurred'}
        ]
        self.sample_alerts = [
            {'timestamp': 1623456795, 'description': 'Alert 1 triggered'},
            {'timestamp': 1623456810, 'description': 'Alert 2 triggered'}
        ]
        self.generator = ReportGenerator(self.sample_events, self.sample_alerts)

    def test_generate_timeline(self):
        timeline = self.generator.generate_timeline()
        self.assertIn("Event 1 occurred", timeline)
        self.assertIn("Alert 1 triggered", timeline)

    def test_highlight_patterns(self):
        patterns = self.generator.highlight_patterns()
        self.assertIn("Pattern detection logic", patterns)

    def test_suggest_remediations(self):
        remediations = self.generator.suggest_remediations()
        self.assertIn("Remediation suggestions", remediations)

    def test_generate_report(self):
        report = self.generator.generate_report()
        self.assertIn("Event Timeline", report)
        self.assertIn("Pattern Analysis", report)
        self.assertIn("Remediation Suggestions", report)

if __name__ == '__main__':
    unittest.main()