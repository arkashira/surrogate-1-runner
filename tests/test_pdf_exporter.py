import os
import unittest
from reports.pdf_exporter import generate_audit_report

class TestPDFExporter(unittest.TestCase):
    def setUp(self):
        self.test_output_dir = '/tmp/test_audit_reports'
        self.sample_report_data = {
            "Report ID": "RPT-TEST-001",
            "Date": "2023-10-01",
            "Description": "This is a test audit evidence report."
        }

    def tearDown(self):
        if os.path.exists(self.test_output_dir):
            for filename in os.listdir(self.test_output_dir):
                file_path = os.path.join(self.test_output_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)

    def test_generate_audit_report(self):
        report_filename = generate_audit_report(self.sample_report_data, self.test_output_dir)
        self.assertTrue(os.path.exists(report_filename))
        self.assertTrue(report_filename.endswith('.pdf'))

if __name__ == '__main__':
    unittest.main()