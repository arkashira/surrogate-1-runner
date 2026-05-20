import unittest
from src.report_formatter import ReportFormatter

class TestReportFormatter(unittest.TestCase):
    def setUp(self):
        self.coverage_data = {
            "overall_coverage": 85,
            "files": [
                {
                    "file": "src/main.py",
                    "uncovered_lines": 10,
                    "recommended_tests": "Test main function with edge cases"
                },
                {
                    "file": "src/utils.py",
                    "uncovered_lines": 5,
                    "recommended_tests": "Test utility functions with various inputs"
                }
            ]
        }
        self.formatter = ReportFormatter(self.coverage_data)

    def test_generate_json_report(self):
        json_report = self.formatter.generate_json_report()
        self.assertIn('"overall_coverage": 85', json_report)
        self.assertIn('"file": "src/main.py"', json_report)

    def test_generate_markdown_report(self):
        markdown_report = self.formatter.generate_markdown_report()
        self.assertIn("Overall Coverage: 85%", markdown_report)
        self.assertIn("src/main.py", markdown_report)
        self.assertIn("Test main function with edge cases", markdown_report)

    def test_generate_reports(self):
        json_report, markdown_report = self.formatter.generate_reports()
        self.assertIsInstance(json_report, str)
        self.assertIsInstance(markdown_report, str)
        self.assertIn('"overall_coverage": 85', json_report)
        self.assertIn("Overall Coverage: 85%", markdown_report)

if __name__ == '__main__':
    unittest.main()