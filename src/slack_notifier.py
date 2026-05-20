import requests
import json

class SlackNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_report(self, report):
        if self.webhook_url:
            headers = {'Content-Type': 'application/json'}
            data = {'text': report}
            response = requests.post(self.webhook_url, headers=headers, data=json.dumps(data))
            if response.status_code != 200:
                print(f"Failed to send report to Slack: {response.text}")
        else:
            print("Slack webhook URL is not configured")

def get_slack_webhook_url(config):
    return config.get('slack', {}).get('webhook_url')

def send_report_to_slack(config, report):
    webhook_url = get_slack_webhook_url(config)
    notifier = SlackNotifier(webhook_url)
    notifier.send_report(report)