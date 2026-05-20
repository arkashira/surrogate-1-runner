import unittest
import unittest.mock as mock
from src.cli import main
from io import StringIO
import sys

class TestCLI(unittest.TestCase):
    @mock.patch.dict(os.environ, {"TENANT_TOKEN": "test_token"})
    @mock.patch("src.cli.generate_investor_report")
    def test_success(self, mock_report):
        mock_report.return_value = "test.pdf"
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        main()
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), "Investor report generated and saved to test.pdf\n")

    @mock.patch.dict(os.environ, clear=True)
    def test_missing_token(self):
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        main()
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), "Error: Tenant token is missing.\n")

    @mock.patch("src.cli.generate_investor_report")
    def test_api_error(self, mock_report):
        mock_report.side_effect = Exception("API error")
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        main()
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), "Error generating report: API error\n")

if __name__ == "__main__":
    unittest.main()