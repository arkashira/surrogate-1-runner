import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

logging.basicConfig(level=logging.INFO)

class AlertService:
    def __init__(self, email_config, in_app_config):
        self.email_config = email_config
        self.in_app_config = in_app_config

    def send_email(self, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.email_config['from']
        msg['To'] = self.email_config['to']
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
        server.starttls()
        server.login(msg['From'], self.email_config['password'])
        text = msg.as_string()
        server.sendmail(msg['From'], msg['To'], text)
        server.quit()

    def send_in_app_notification(self, subject, body):
        requests.post(self.in_app_config['url'], json={'subject': subject, 'body': body})

def configure_alerts(email_config, in_app_config):
    alert_service = AlertService(email_config, in_app_config)
    return alert_service

email_config = {
    'from': 'your-email@example.com',
    'to': 'recipient-email@example.com',
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587,
    'password': 'your-password'
}

in_app_config = {
    'url': 'https://your-in-app-notification-url.com'
}

alert_service = configure_alerts(email_config, in_app_config)