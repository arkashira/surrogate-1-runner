import requests
from .models.alert import Alert

class WebhookNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_alert(self, alert: Alert):
        payload = {
            'text': str(alert),
            'attachments': [
                {
                    'fallback': alert.message,
                    'color': '#FF0000',
                    'fields': [
                        {
                            'title': 'Message',
                            'value': alert.message,
                            'short': False
                        },
                        {
                            'title': 'Timestamp',
                            'value': alert.timestamp.isoformat(),
                            'short': True
                        }
                    ]
                }
            ]
        }
        response = requests.post(self.webhook_url, json=payload)
        response.raise_for_status()
        return response.status_code == 200