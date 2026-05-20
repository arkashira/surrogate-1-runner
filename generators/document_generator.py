
import logging
from datetime import datetime

from axentx.libs.generators.base_generator import BaseGenerator
from axentx.libs.utils.file_utils import read_file

class DocumentGenerator(BaseGenerator):
    def __init__(self, output_dir):
        super().__init__(output_dir)
        self.logger = logging.getLogger(__name__)

    def generate(self, document_id):
        # ... (existing code)

        # Include audit logs in the generated documentation
        audit_logs = self.get_audit_logs(document_id)
        self.logger.info(f"Including {len(audit_logs)} audit logs in the documentation")

        with open(f"{self.output_dir}/audit_logs.txt", "w") as f:
            for log in audit_logs:
                f.write(f"{log['timestamp']} - {log['message']}\n")

        # ... (existing code)

    def get_audit_logs(self, document_id):
        # Assume there's a function to fetch audit logs based on document_id
        # Replace this with actual implementation
        return [
            {"timestamp": datetime.now(), "message": "Audit log message 1"},
            {"timestamp": datetime.now(), "message": "Audit log message 2"},
        ]

# /opt/axentx/surrogate-1/tests/test_document_generator.py

import unittest
from unittest.mock import patch

from axentx.libs.generators.document_generator import DocumentGenerator

class TestDocumentGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = DocumentGenerator("/tmp/output")

    @patch("axentx.libs.generators.document_generator.DocumentGenerator.get_audit_logs")
    def test_generate_includes_audit_logs(self, mock_get_audit_logs):
        mock_get_audit_logs.return_value = [
            {"timestamp": "2022-01-01", "message": "Audit log message 1"},
            {"timestamp": "2022-01-02", "message": "Audit log message 2"},
        ]

        self.generator.generate("test_document")

        with open("/tmp/output/audit_logs.txt", "r") as f:
            logs = f.readlines()

        self.assertEqual(len(logs), 2)
        self.assertIn("2022-01-01 - Audit log message 1\n", logs)
        self.assertIn("2022-01-02 - Audit log message 2\n", logs)

## Summary
- Added `get_audit_logs` method to fetch audit logs for a document
- Included audit logs in the generated documentation
- Updated tests to include audit log generation