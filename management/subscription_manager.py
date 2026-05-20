import json
from typing import Dict

class SubscriptionManager:
    def __init__(self):
        self.subscriptions: Dict[str, bool] = {}

    def add_subscription(self, user_id: str, is_paid: bool):
        self.subscriptions[user_id] = is_paid

    def get_subscription(self, user_id: str) -> bool:
        return self.subscriptions.get(user_id, False)

    def update_subscription(self, user_id: str, is_paid: bool):
        self.subscriptions[user_id] = is_paid

    def save_state(self):
        with open('subscriptions.json', 'w') as f:
            json.dump(self.subscriptions, f)

    def load_state(self):
        try:
            with open('subscriptions.json', 'r') as f:
                self.subscriptions = json.load(f)
        except FileNotFoundError:
            pass

# tests
# opt/axentx/surrogate-1/management/test_subscription_manager.py
import unittest
from subscription_manager import SubscriptionManager

class TestSubscriptionManager(unittest.TestCase):
    def setUp(self):
        self.manager = SubscriptionManager()

    def test_add_subscription(self):
        self.manager.add_subscription('user1', True)
        self.assertTrue(self.manager.get_subscription('user1'))

    def test_get_subscription(self):
        self.manager.add_subscription('user1', True)
        self.assertTrue(self.manager.get_subscription('user1'))

    def test_update_subscription(self):
        self.manager.add_subscription('user1', True)
        self.manager.update_subscription('user1', False)
        self.assertFalse(self.manager.get_subscription('user1'))

if __name__ == '__main__':
    unittest.main()