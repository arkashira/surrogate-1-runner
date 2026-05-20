import os
import unittest
from unittest.mock import patch, mock_open
from report_generator import generate_html_report
import json

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.account_id = "test_account"
        self.report_dir = f"/opt/axentx/surrogate-1/reports/{self.account_id}"
        self.report_path = f"{self.report_dir}/compliance.html"
        self.template_path = "templates/compliance_report_template.html"

        # Create a mock compliance report
        self.mock_report = {
            "summary": {
                "total_checks": 10,
                "passed_checks": 8,
                "failed_checks": 2,
                "skipped_checks": 0
            },
            "checks": [
                {
                    "id": "check1",
                    "name": "Check 1",
                    "status": "passed",
                    "timestamp": "2023-01-01T00:00:00Z"
                },
                {
                    "id": "check2",
                    "name": "Check 2",
                    "status": "failed",
                    "timestamp": "2023-01-01T00:00:01Z"
                }
            ],
            "metadata": {
                "account_id": self.account_id,
                "generated_at": "2023-01-01T00:00:00Z"
            }
        }

    def test_generate_html_report(self):
        # Mock the template file
        mock_template = """
        <html>
            <body>
                <h1>Compliance Report</h1>
                <div id="summary">{{ summary }}</div>
                <div id="checks">{{ checks }}</div>
                <div id="metadata">{{ metadata }}</div>
            </body>
        </html>
        """

        # Mock the open function to return our mock template
        with patch("builtins.open", mock_open(read_data=mock_template)):
            # Call the function to test
            generate_html_report(self.mock_report, self.account_id)

            # Assert the report file was created
            self.assertTrue(os.path.exists(self.report_path))

            # Read the report file
            with open(self.report_path, "r") as f:
                report_content = f.read()

            # Assert the report content contains the expected data
            self.assertIn("Compliance Report", report_content)
            self.assertIn("total_checks: 10", report_content)
            self.assertIn("Check 1", report_content)
            self.assertIn("Check 2", report_content)
            self.assertIn("account_id: test_account", report_content)

    def tearDown(self):
        # Clean up the report file and directory
        if os.path.exists(self.report_path):
            os.remove(self.report_path)
        if os.path.exists(self.report_dir):
            os.rmdir(self.report_dir)

if __name__ == "__main__":
    unittest.main()