import unittest
from unittest.mock import patch
from src.diagnostic_reporter import DiagnosticReporter

class TestDiagnosticReporter(unittest.TestCase):
    def test_map_exit_codes(self):
        diagnostic_reporter = DiagnosticReporter({})
        exit_code_map = diagnostic_reporter.map_exit_codes(1)
        self.assertEqual(exit_code_map, "Cannot connect to PostgreSQL server")

    def test_generate_failure_report(self):
        diagnostic_reporter = DiagnosticReporter({})
        exit_code = 1
        stack_trace = "Traceback (most recent call last):\n  File \"main.py\", line 1, in <module>\n    raise ValueError('Invalid password')\nValueError: Invalid password"
        config_diff = {
            "database_name": "my_database",
            "username": "my_username",
            "password": "wrong_password",
        }
        report = diagnostic_reporter.generate_failure_report(exit_code, stack_trace, config_diff)
        self.assertIsInstance(report, str)

    def test_integrate_with_error_reporting_system(self):
        with patch("subprocess.run") as mock_run:
            diagnostic_reporter = DiagnosticReporter({})
            exit_code = 1
            stack_trace = "Traceback (most recent call last):\n  File \"main.py\", line 1, in <module>\n    raise ValueError('Invalid password')\nValueError: Invalid password"
            config_diff = {
                "database_name": "my_database",
                "username": "my_username",
                "password": "wrong_password",
            }
            diagnostic_reporter.integrate_with_error_reporting_system(diagnostic_reporter.generate_failure_report(exit_code, stack_trace, config_diff))
            mock_run.assert_called_once()

if __name__ == "__main__":
    unittest.main()