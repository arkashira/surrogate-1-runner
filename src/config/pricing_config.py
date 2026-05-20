class PricingConfig:
    def __init__(self):
        self.free_tier_features = {
            "cloud_accounts": 5,
            "alerting": "basic"
        }
        self.usage_limits = {
            "cloud_accounts": 5,
            "alerting": "basic"
        }
        self.upgrade_path = "https://example.com/upgrade"

    def get_free_tier_features(self):
        return self.free_tier_features

    def get_usage_limits(self):
        return self.usage_limits

    def get_upgrade_path(self):
        return self.upgrade_path