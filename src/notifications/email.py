import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailNotification:
    def __init__(self, smtp_server, port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_alert(self, recipient_email, subject, message):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(self.smtp_server, self.port)
        server.starttls()
        server.login(self.sender_email, self.sender_password)
        text = msg.as_string()
        server.sendmail(self.sender_email, recipient_email, text)
        server.quit()

    def send_cost_alert(self, recipient_email, alert_message):
        subject = "Predictive Cost Alert"
        self.send_alert(recipient_email, subject, alert_message)


# /opt/axentx/surrogate-1/src/notifications/in_app.py
import requests

class InAppNotification:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def send_alert(self, message):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'title': "Predictive Cost Alert",
            'message': message
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        if response.status_code != 200:
            print(f"Error sending notification: {response.text}")

    def send_cost_alert(self, alert_message):
        self.send_alert(alert_message)


# /opt/axentx/surrogate-1/src/predictive_cost_alerts.py
from notifications.email import EmailNotification
from notifications.in_app import InAppNotification

class PredictiveCostAlerts:
    def __init__(self, email_notifier, in_app_notifier):
        self.email_notifier = email_notifier
        self.in_app_notifier = in_app_notifier

    def send_alerts(self, to_email, alert_message):
        self.email_notifier.send_cost_alert(to_email, alert_message)
        self.in_app_notifier.send_cost_alert(alert_message)

# Example usage:
email_notifier = EmailNotification('smtp.example.com', 587, 'sender@example.com', 'password')
in_app_notifier = InAppNotification('https://api.example.com/notifications', 'api_key')
predictive_cost_alerts = PredictiveCostAlerts(email_notifier, in_app_notifier)
predictive_cost_alerts.send_alerts('recipient@example.com', 'Your predicted costs are rising. Recommended action: Review usage patterns.')