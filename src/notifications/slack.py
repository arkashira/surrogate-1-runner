import requests
import json

class SlackNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_alert(self, alert_payload):
        message = self._format_message(alert_payload)
        response = requests.post(
            self.webhook_url,
            data=json.dumps(message),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(f'Request to slack returned an error {response.status_code}, the response is:\n{response.text}')

    def _format_message(self, alert_payload):
        return {
            "text": f"Cost anomaly detected!\nAccount ID: {alert_payload['account_id']}\nService: {alert_payload['service']}\nCurrent Cost: {alert_payload['current_cost']}\nPrevious Avg: {alert_payload['previous_avg']}\n% Change: {alert_payload['percentage_change']}%\nDashboard Link: {alert_payload['dashboard_link']}"
        }

# Example usage
if __name__ == "__main__":
    notifier = SlackNotifier("YOUR_SLACK_WEBHOOK_URL")
    alert_payload = {
        "account_id": "12345",
        "service": "Storage",
        "current_cost": 150.0,
        "previous_avg": 100.0,
        "percentage_change": 50,
        "dashboard_link": "http://example.com/dashboard"
    }
    notifier.send_alert(alert_payload)