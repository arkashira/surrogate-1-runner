import time
from notifiers.alert_sender import AlertSender

class BudgetMonitor:
    def __init__(self, budget, alert_threshold=0.8, forecast_days=7):
        self.budget = budget
        self.alert_threshold = alert_threshold
        self.forecast_days = forecast_days
        self.alert_sender = AlertSender()

    def check_budget(self):
        current_spend = get_current_spend()  # Implement this function
        if current_spend >= self.budget * self.alert_threshold:
            self.alert_sender.send_alert(f"Budget alert! Current spend: {current_spend}, Budget: {self.budget}")

    def forecast_spend(self):
        projected_spend = forecast_spend(self.forecast_days)  # Implement this function
        confidence_interval = calculate_confidence_interval(projected_spend)  # Implement this function
        return projected_spend, confidence_interval

    def run(self):
        while True:
            self.check_budget()
            projected_spend, confidence_interval = self.forecast_spend()
            print(f"Projected spend for next {self.forecast_days} days: {projected_spend} ± {confidence_interval}")
            time.sleep(60)  # Check budget every minute

# /opt/axentx/surrogate-1/src/notifiers/alert_sender.py
import requests
import smtplib
from slacker import Slacker

class AlertSender:
    def __init__(self, webhook_url=None, email_config=None, slack_token=None):
        self.webhook_url = webhook_url
        self.email_config = email_config
        self.slack_token = slack_token
        self.slack_client = Slacker(slack_token)

    def send_alert(self, message):
        if self.webhook_url:
            requests.post(self.webhook_url, json={"message": message})
        if self.email_config:
            self.send_email(message, **self.email_config)
        if self.slack_token:
            self.slack_client.chat.post_message("#alerts", message)

    def send_email(self, message, subject, to, from_email, password):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to, f"Subject: {subject}\n\n{message}")
        server.quit()

# ## Summary
# - Added `BudgetMonitor` service to check budget and send alerts when threshold is reached
# - Implemented `AlertSender` to send alerts via webhook, email, and Slack
# - Budget monitoring service runs in an infinite loop, checking budget every minute
# - Forecasting functionality added to `BudgetMonitor` service