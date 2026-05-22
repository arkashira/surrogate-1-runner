import smtplib
from email.mime.text import MIMEText
import requests

SLACK_WEBHOOK_URL = '<slack-webhook>'
EMAIL_CONFIG = {
    'smtp_server': 'smtp.example.com',
    'port': 587,
    'sender_email': 'alert@example.com',
    'receiver_email': 'developer@example.com',
    'password': 'your-email-password'
}

def send_slack_message(message):
    payload = {'text': message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        raise ValueError(f'Slack notification failed with status code {response.status_code}')

def send_email_message(message):
    msg = MIMEText(message)
    msg['Subject'] = 'Vulnerability Alert'
    msg['From'] = EMAIL_CONFIG['sender_email']
    msg['To'] = EMAIL_CONFIG['receiver_email']

    with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['port']) as server:
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['password'])
        server.sendmail(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['receiver_email'], msg.as_string())

def send_alert(source, message):
    print(f'Alert from {source}: {message}')
    send_slack_message(message)
    send_email_message(message)