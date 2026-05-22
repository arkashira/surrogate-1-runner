import os
import unittest
from src.budget_tracker import BudgetTracker, BudgetNotification

class TestBudgetTracker(unittest.TestCase):
    def setUp(self):
        self.budget_file = 'test_budget.json'
        self.budget_tracker = BudgetTracker(self.budget_file)

    def tearDown(self):
        if os.path.exists(self.budget_file):
            os.remove(self.budget_file)

    def test_set_and_get_budget(self):
        self.budget_tracker.set_budget(1000.0)
        self.assertEqual(self.budget_tracker.get_budget(), 1000.0)

    def test_add_and_get_expenses(self):
        self.budget_tracker.add_expense(100.0, 'Server costs')
        self.budget_tracker.add_expense(200.0, 'Storage costs')
        expenses = self.budget_tracker.get_expenses()
        self.assertEqual(len(expenses), 2)
        self.assertEqual(expenses[0]['amount'], 100.0)
        self.assertEqual(expenses[1]['amount'], 200.0)

    def test_get_remaining_budget(self):
        self.budget_tracker.set_budget(1000.0)
        self.budget_tracker.add_expense(100.0, 'Server costs')
        self.budget_tracker.add_expense(200.0, 'Storage costs')
        self.assertEqual(self.budget_tracker.get_remaining_budget(), 700.0)

    def test_detect_anomalies(self):
        self.budget_tracker.add_expense(100.0, 'Server costs')
        self.budget_tracker.add_expense(200.0, 'Storage costs')
        self.budget_tracker.add_expense(300.0, 'Network costs')
        self.budget_tracker.add_expense(1000.0, 'Unexpected expense')
        anomalies = self.budget_tracker.detect_anomalies()
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['amount'], 1000.0)

class TestBudgetNotification(unittest.TestCase):
    def test_send_notification(self):
        # This is a mock test. In a real scenario, you would need to set up a mock SNS client.
        notification = BudgetNotification('arn:aws:sns:us-east-1:123456789012:BudgetAnomalies')
        try:
            notification.send_notification('Test message')
        except Exception as e:
            self.fail(f"Notification sending failed: {e}")

if __name__ == '__main__':
    unittest.main()