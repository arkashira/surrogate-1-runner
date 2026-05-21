import unittest
from unittest.mock import MagicMock
from github import Github
from src.github.comments import ComplianceScanner

class TestComplianceScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = ComplianceScanner('fake_token', 'owner/repo')
        self.scanner.repo = MagicMock()
        self.scanner.repo.get_pull = MagicMock(return_value=MagicMock(create_issue_comment=MagicMock()))

    def test_post_scan_summary_no_violations(self):
        self.scanner.post_scan_summary(1, [])
        self.scanner.repo.get_pull().create_issue_comment.assert_called_once_with("All compliance checks passed.")

    def test_post_scan_summary_with_violations(self):
        violations = ["Violation 1", "Violation 2"]
        self.scanner.post_scan_summary(1, violations)
        self.scanner.repo.get_pull().create_issue_comment.assert_called_once_with("Compliance violations found:\nViolation 1\nViolation 2")

if __name__ == '__main__':
    unittest.main()