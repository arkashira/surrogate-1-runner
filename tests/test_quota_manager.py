import unittest
from src.quota_manager import QuotaManager

class TestQuotaManager(unittest.TestCase):
    def test_get_quota(self):
        quota_manager = QuotaManager()
        self.assertEqual(quota_manager.get_quota('user1'), 2)

    def test_update_usage(self):
        quota_manager = QuotaManager()
        quota_manager.update_usage('user1', 1)
        self.assertEqual(quota_manager.get_quota('user1'), 1)

    def test_reset_quota(self):
        quota_manager = QuotaManager()
        quota_manager.update_usage('user1', 1)
        quota_manager.reset_quota()
        self.assertEqual(quota_manager.get_quota('user1'), 2)

    def test_save_usage(self):
        quota_manager = QuotaManager()
        quota_manager.update_usage('user1', 1)
        quota_manager.save_usage()
        with open('/opt/axentx/surrogate-1/data/usage.json', 'r') as f:
            usage = json.load(f)
        self.assertEqual(usage['user1'], 1)

    def test_load_usage(self):
        quota_manager = QuotaManager()
        quota_manager.update_usage('user1', 1)
        quota_manager.save_usage()
        quota_manager.load_usage()
        self.assertEqual(quota_manager.usage['user1'], 1)

    def test_check_quota(self):
        quota_manager = QuotaManager()
        self.assertTrue(quota_manager.check_quota('user1'))
        quota_manager.update_usage('user1', 2)
        self.assertFalse(quota_manager.check_quota('user1'))