import unittest
import os
import json
from tap.coverage_report import generate_coverage_report

class TestCoverageReport(unittest.TestCase):
    def setUp(self):
        self.original_coverage_data = [
            {"filename": "module1.py", "covered_lines": [1, 2, 3], "num_statements": 5, "percent_covered": 60},
            {"filename": "module2.py", "covered_lines": [1, 2, 3, 4, 5], "num_statements": 5, "percent_covered": 100}
        ]
        self.expected_report_content = {
            "generated_at": None,
            "coverage_summary": {
                "module1.py": {"covered_lines": 3, "num_statements": 5, "percent_covered": 60},
                "module2.py": {"covered_lines": 5, "num_statements": 5, "percent_covered": 100}
            },
            "missing_coverage": [
                {"module": "module1.py", "missing_lines": [4, 5]}
            ]
        }

    def tearDown(self):
        # Clean up any generated report files
        for filename in os.listdir('.'):
            if filename.startswith('coverage_report_') and filename.endswith('.json'):
                os.remove(filename)

    def test_generate_coverage_report(self):
        # Mock the coverage report data
        with open('coverage.json', 'w') as coverage_file:
            json.dump(self.original_coverage_data, coverage_file)

        # Generate the coverage report
        generate_coverage_report()

        # Find the generated report file
        report_files = [filename for filename in os.listdir('.') if filename.startswith('coverage_report_') and filename.endswith('.json')]
        self.assertEqual(len(report_files), 1)

        # Read and validate the report content
        with open(report_files[0], 'r') as report_file:
            report_content = json.load(report_file)

        self.assertIsNotNone(report_content["generated_at"])
        self.assertDictEqual(report_content["coverage_summary"], self.expected_report_content["coverage_summary"])
        self.assertListEqual(report_content["missing_coverage"], self.expected_report_content["missing_coverage"])

if __name__ == "__main__":
    unittest.main()