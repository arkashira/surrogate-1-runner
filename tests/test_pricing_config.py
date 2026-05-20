import unittest
from surrogate_1.src.config import get_pricing_config

class TestPricingConfig(unittest.TestCase):
    def test_get_free_tier_features(self):
        pricing_config = get_pricing_config()
        self.assertEqual(pricing_config.get_free_tier_features(), {"cloud_accounts": 5, "alerting": "basic"})

    def test_get_usage_limits(self):
        pricing_config = get_pricing_config()
        self.assertEqual(pricing_config.get_usage_limits(), {"cloud_accounts": 5, "alerting": "basic"})

    def test_get_upgrade_path(self):
        pricing_config = get_pricing_config()
        self.assertEqual(pricing_config.get_upgrade_path(), "https://example.com/upgrade")