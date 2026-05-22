import datetime
import json
import os
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

class BudgetTracker:
    def __init__(self, budget_file: str = 'budget.json'):
        self.budget_file = budget_file
        self.budget_data = self._load_budget_data()

    def _load_budget_data(self) -> Dict:
        if os.path.exists(self.budget_file):
            with open(self.budget_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_budget_data(self) -> None:
        with open(self.budget_file, 'w') as f:
            json.dump(self.budget_data, f)

    def set_budget(self, budget: float) -> None:
        self.budget_data['budget'] = budget
        self._save_budget_data()

    def get_budget(self) -> Optional[float]:
        return self.budget_data.get('budget')

    def add_expense(self, amount: float, description: str) -> None:
        if 'expenses' not in self.budget_data:
            self.budget_data['expenses'] = []

        expense = {
            'amount': amount,
            'description': description,
            'date': datetime.datetime.now().isoformat()
        }
        self.budget_data['expenses'].append(expense)
        self._save_budget_data()

    def get_expenses(self) -> List[Dict]:
        return self.budget_data.get('expenses', [])

    def get_remaining_budget(self) -> Optional[float]:
        budget = self.get_budget()
        if budget is None:
            return None

        total_expenses = sum(expense['amount'] for expense in self.get_expenses())
        return budget - total_expenses

    def detect_anomalies(self) -> List[Dict]:
        expenses = self.get_expenses()
        if not expenses:
            return []

        # Calculate average and standard deviation of expenses
        amounts = [expense['amount'] for expense in expenses]
        avg = sum(amounts) / len(amounts)
        std_dev = (sum((x - avg) ** 2 for x in amounts) / len(amounts)) ** 0.5

        # Identify anomalies (expenses that are more than 2 standard deviations from the mean)
        anomalies = [expense for expense in expenses if abs(expense['amount'] - avg) > 2 * std_dev]

        return anomalies

class BudgetNotification:
    def __init__(self, sns_topic_arn: str):
        self.sns_client = boto3.client('sns')
        self.sns_topic_arn = sns_topic_arn

    def send_notification(self, message: str) -> None:
        try:
            response = self.sns_client.publish(
                TopicArn=self.sns_topic_arn,
                Message=message,
                Subject='Budget Anomaly Detected'
            )
            print(f"Notification sent. Message ID: {response['MessageId']}")
        except ClientError as e:
            print(f"Error sending notification: {e}")

# Example usage
if __name__ == '__main__':
    budget_tracker = BudgetTracker()
    budget_tracker.set_budget(1000.0)

    # Add some expenses
    budget_tracker.add_expense(100.0, 'Server costs')
    budget_tracker.add_expense(200.0, 'Storage costs')
    budget_tracker.add_expense(300.0, 'Network costs')

    # Detect anomalies
    anomalies = budget_tracker.detect_anomalies()
    print(f"Anomalies detected: {anomalies}")

    # Send notifications
    if anomalies:
        notification = BudgetNotification('arn:aws:sns:us-east-1:123456789012:BudgetAnomalies')
        notification.send_notification(f"Anomalies detected in budget: {anomalies}")