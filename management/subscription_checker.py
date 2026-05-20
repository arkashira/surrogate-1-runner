import subscription_manager

class SubscriptionChecker:
    def __init__(self):
        self.manager = subscription_manager.SubscriptionManager()
        self.manager.load_state()

    def check_subscription(self, user_id: str) -> bool:
        return self.manager.get_subscription(user_id)

    def update_subscription(self, user_id: str, is_paid: bool):
        self.manager.update_subscription(user_id, is_paid)
        self.manager.save_state()

# tests
# opt/axentx/surrogate-1/management/test_subscription_checker.py
import unittest
from subscription_checker import SubscriptionChecker

class TestSubscriptionChecker(unittest.TestCase):
    def setUp(self):
        self.checker = SubscriptionChecker()

    def test_check_subscription(self):
        self.checker.update_subscription('user1', True)
        self.assertTrue(self.checker.check_subscription('user1'))

    def test_update_subscription(self):
        self.checker.update_subscription('user1', True)
        self.checker.update_subscription('user1', False)
        self.assertFalse(self.checker.check_subscription('user1'))

if __name__ == '__main__':
    unittest.main()