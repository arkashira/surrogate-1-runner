import unittest
import os
import json
from datetime import datetime
from command_logger import CommandLogger

class TestCommandLogger(unittest.TestCase):
    def setUp(self):
        self.test_log_dir = '/tmp/test_audit_logs'
        os.makedirs(self.test_log_dir, exist_ok=True)
        self.logger = CommandLogger(log_dir=self.test_log_dir)

    def tearDown(self):
        for file in os.listdir(self.test_log_dir):
            os.remove(os.path.join(self.test_log_dir, file))
        os.rmdir(self.test_log_dir)

    def test_log_command(self):
        command = "test_command"
        user_identity = "test_user"
        session_metadata = {"session_id": "12345"}

        self.logger.log_command(command, user_identity, session_metadata)

        log_files = os.listdir(self.test_log_dir)
        self.assertEqual(len(log_files), 1)

        log_file = os.path.join(self.test_log_dir, log_files[0])
        with open(log_file, 'r') as f:
            log_entry = json.load(f)

        self.assertEqual(log_entry['command'], command)
        self.assertEqual(log_entry['user_identity'], user_identity)
        self.assertEqual(log_entry['session_metadata'], session_metadata)
        self.assertTrue('timestamp' in log_entry)

if __name__ == '__main__':
    unittest.main()