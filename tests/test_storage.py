import os
import json
import csv
import unittest
from storage import SecureLogStorage

class TestSecureLogStorage(unittest.TestCase):
    def setUp(self):
        self.storage = SecureLogStorage(log_dir="test_logs")
        self.user_details = {"username": "admin", "role": "IT Administrator"}
        self.model_access = {"model_name": "AI Model", "access_type": "read"}

    def tearDown(self):
        for f in os.listdir(self.storage.log_dir):
            os.remove(os.path.join(self.storage.log_dir, f))
        os.rmdir(self.storage.log_dir)

    def test_log_access(self):
        self.storage.log_access(self.user_details, self.model_access)
        log_files = [f for f in os.listdir(self.storage.log_dir) if f.endswith('.json')]
        self.assertEqual(len(log_files), 1)
        with open(os.path.join(self.storage.log_dir, log_files[0]), 'r') as f:
            log_entry = json.load(f)
        self.assertEqual(log_entry["user_details"], self.user_details)
        self.assertEqual(log_entry["model_access"], self.model_access)

    def test_export_logs_csv(self):
        self.storage.log_access(self.user_details, self.model_access)
        output_file = "test_access_logs.csv"
        self.storage.export_logs("csv", output_file)
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["user_details"], json.dumps(self.user_details))
        self.assertEqual(rows[0]["model_access"], json.dumps(self.model_access))
        os.remove(output_file)

    def test_export_logs_json(self):
        self.storage.log_access(self.user_details, self.model_access)
        output_file = "test_access_logs.json"
        self.storage.export_logs("json", output_file)
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r') as f:
            logs = json.load(f)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["user_details"], self.user_details)
        self.assertEqual(logs[0]["model_access"], self.model_access)
        os.remove(output_file)

if __name__ == "__main__":
    unittest.main()