
import unittest
from unittest.mock import MagicMock, patch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reports import generate_incident_report

class TestReports(unittest.TestCase):
    def test_generate_incident_report(self):
        data = {"incident_id": "12345", "timestamp": "2026-05-03 12:34:56", "severity": "high"}
        preferences = {"report_format": "PDF", "output_directory": "/path/to/output"}

        with patch("sys.stdout", new=MagicMock()) as mock_stdout:
            generate_incident_report(data, preferences)
            mock_stdout.write.assert_called_once_with(b"Saving incident report to /path/to/output/incident_report_20260503_123456.pdf")

        doc_path = f"/path/to/output/incident_report_20260503_123456.pdf"
        with open(doc_path, "rb") as file:
            report = file.read()

        self.assertGreater(len(report), 0)

        os.remove(doc_path)

if __name__ == "__main__":
    unittest.main()