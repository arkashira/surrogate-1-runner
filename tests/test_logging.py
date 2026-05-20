import unittest
from src.logging import AIModelUsageLogger
from src.db import DBHandler

class TestAIModelUsageLogger(unittest.TestCase):
    def setUp(self):
        self.db_handler = DBHandler(':memory:')  # Use an in-memory database for testing
        self.logger = AIModelUsageLogger(self.db_handler)

    def test_log_usage(self):
        user_id = 'test_user'
        model_name = 'test_model'
        usage_details = {'input': 'test_input', 'output': 'test_output'}
        self.logger.log_usage(user_id, model_name, usage_details)
        
        logs = self.db_handler.get_logs()
        self.assertEqual(len(logs), 1)
        log_entry = logs[0]
        self.assertEqual(log_entry[1], user_id)
        self.assertEqual(log_entry[2], model_name)
        self.assertIn(str(usage_details), log_entry[3])

if __name__ == '__main__':
    unittest.main()