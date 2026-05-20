import smtplib
from email.mime.text import MIMEText
from src.config import EMAIL_CONFIG

def send_email_alert(message, recipient):
    """Send email alert with cost information"""
    msg = MIMEText(message)
    msg['Subject'] = 'Cloud Cost Alert'
    msg['From'] = EMAIL_CONFIG['sender']
    msg['To'] = recipient

    with smtplib.SMTP_SSL(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['port']) as server:
        server.login(EMAIL_CONFIG['sender'], EMAIL_CONFIG['password'])
        server.sendmail(EMAIL_CONFIG['sender'], recipient, msg.as_string())