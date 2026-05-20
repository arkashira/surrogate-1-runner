import smtplib
from email.mime.text import MIMEText

def send_alert(user_id, action):
    msg = MIMEText(f'Unauthorized access attempt by user {user_id} for action: {action}')
    msg['Subject'] = 'Unauthorized Access Alert'
    msg['From'] = 'admin@axentx.com'
    msg['To'] = 'security@axentx.com'

    with smtplib.SMTP('localhost') as server:
        server.send_message(msg)