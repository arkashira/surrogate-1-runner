import os
import json
from coverage import Coverage

class CoverageReporter:
    def __init__(self, data_file):
        self.data_file = data_file
        self.coverage = Coverage(data_file)

    def generate_report(self, output_dir):
        self.coverage.load()
        self.coverage.save()

        html_report = os.path.join(output_dir, 'coverage.html')
        json_report = os.path.join(output_dir, 'coverage.json')
        xml_report = os.path.join(output_dir, 'coverage.xml')

        self.coverage.html_report(directory=output_dir)
        self.coverage.json_report(outfile=json_report)
        self.coverage.xml_report(outfile=xml_report)

        print(f"Coverage reports generated and saved to {output_dir}")

    def export_report(self, output_dir, format='html'):
        if format == 'html':
            self.coverage.html_report(directory=output_dir)
        elif format == 'json':
            self.coverage.json_report(outfile=os.path.join(output_dir, 'coverage.json'))
        elif format == 'xml':
            self.coverage.xml_report(outfile=os.path.join(output_dir, 'coverage.xml'))
        else:
            raise ValueError("Invalid report format")

# src/core/test_runner.py
import unittest
from reporting.coverage_reporter import CoverageReporter

class TestRunner:
    def __init__(self, test_dir):
        self.test_dir = test_dir

    def run_tests(self):
        suite = unittest.defaultTestLoader.discover(self.test_dir)
        runner = unittest.TextTestRunner()
        result = runner.run(suite)
        return result.wasSuccessful()

    def generate_coverage_report(self, output_dir, data_file='coverage.data'):
        reporter = CoverageReporter(data_file)
        reporter.generate_report(output_dir)

# test/test_core.py
import unittest
from core.test_runner import TestRunner

class TestRunnerTest(unittest.TestCase):
    def test_run_tests_and_generate_coverage(self):
        test_dir = 'test'
        output_dir = 'test_output'
        test_runner = TestRunner(test_dir)
        success = test_runner.run_tests()
        test_runner.generate_coverage_report(output_dir)
        self.assertTrue(success)

## Summary
- Combined the strengths of both candidates to create a robust coverage reporting system.
- The `CoverageReporter` class generates and exports coverage reports in various formats.
- The `TestRunner` class runs tests and generates coverage reports.
- Reports can be exported in HTML, JSON, or XML formats.