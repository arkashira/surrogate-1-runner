import requests
import json
from datetime import datetime
from .models import AlertLog

class SlackDispatcher:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_alert(self, resource_id, rule_name, severity, dashboard_link):
        payload = {
            "text": f"High Severity Alert: {rule_name}",
            "attachments": [
                {
                    "color": "#FF0000",
                    "fields": [
                        {"title": "Resource ID", "value": resource_id, "short": True},
                        {"title": "Rule Name", "value": rule_name, "short": True},
                        {"title": "Severity", "value": severity, "short": True},
                        {"title": "Dashboard Link", "value": dashboard_link, "short": False}
                    ]
                }
            ]
        }

        response = requests.post(self.webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        
        # Log the alert delivery status
        self.log_delivery_status(response.status_code, resource_id, rule_name)

    def log_delivery_status(self, status_code, resource_id, rule_name):
        log_entry = AlertLog(
            timestamp=datetime.now(),
            resource_id=resource_id,
            rule_name=rule_name,
            delivery_status=status_code
        )
        log_entry.save()

# Example usage
# slack_dispatcher = SlackDispatcher("YOUR_SLACK_WEBHOOK_URL")
# slack_dispatcher.send_alert("RESOURCE_ID", "RULE_NAME", "SEVERITY", "DASHBOARD_LINK")