import unittest
import os
import json
from datetime import datetime
from src.usage_tracker import UsageTracker

class TestUsageTracker(unittest.TestCase):
    def setUp(self):
        self.test_storage_path = '/opt/axentx/surrogate-1/tests/data/test_usage.json'
        self.usage_tracker = UsageTracker(self.test_storage_path)

    def tearDown(self):
        if os.path.exists(self.test_storage_path):
            os.remove(self.test_storage_path)

    def test_track_cloud_account(self):
        user_id = 'test_user'
        cloud_account_id = 'cloud_account_1'

        self.usage_tracker.track_cloud_account(user_id, cloud_account_id)
        self.assertEqual(len(self.usage_tracker.get_cloud_accounts(user_id)), 1)

        # Test adding more than 5 cloud accounts
        for i in range(2, 6):
            self.usage_tracker.track_cloud_account(user_id, f'cloud_account_{i}')

        with self.assertRaises(Exception):
            self.usage_tracker.track_cloud_account(user_id, 'cloud_account_6')

    def test_add_alert(self):
        user_id = 'test_user'
        alert_message = 'Test alert message'

        self.usage_tracker.add_alert(user_id, alert_message)
        alerts = self.usage_tracker.get_alerts(user_id)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]['message'], alert_message)

    def test_load_and_save_usage_data(self):
        user_id = 'test_user'
        cloud_account_id = 'cloud_account_1'
        alert_message = 'Test alert message'

        self.usage_tracker.track_cloud_account(user_id, cloud_account_id)
        self.usage_tracker.add_alert(user_id, alert_message)

        # Create a new instance to test loading from file
        new_usage_tracker = UsageTracker(self.test_storage_path)
        self.assertEqual(len(new_usage_tracker.get_cloud_accounts(user_id)), 1)
        self.assertEqual(len(new_usage_tracker.get_alerts(user_id)), 1)

if __name__ == '__main__':
    unittest.main()