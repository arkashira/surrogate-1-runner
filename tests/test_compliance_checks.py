import unittest
from unittest.mock import patch
from compliance.checks import ComplianceChecker

class TestComplianceChecks(unittest.TestCase):
    @patch('compliance.checks.logging')
    def test_run_checks(self, mock_logging):
        checker = ComplianceChecker()
        checker.run_checks()

        mock_logging.info.assert_any_call("Checking user roles...")
        mock_logging.info.assert_any_call("Logging sessions...")
        mock_logging.info.assert_any_call("Performing compliance checks...")
        mock_logging.info.assert_any_call("All compliance checks passed.")

if __name__ == '__main__':
    unittest.main()