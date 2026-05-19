import smtplib
from email.mime.text import MIMEText

def send_email(user_id, message):
    msg = MIMEText(message)
    msg['Subject'] = 'Compliance Alert'
    msg['From'] = 'noreply@axentx.com'
    msg['To'] = f'user{user_id}@example.com'

    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login('user@example.com', 'password')
    server.sendmail('user@example.com', [msg['To']], msg.as_string())
    server.quit()

def send_sms(user_id, message):
    # Placeholder for SMS sending logic
    print(f"SMS sent to user {user_id}: {message}")

def send_notification(user_id, message, preference):
    if preference == 'email':
        send_email(user_id, message)
    elif preference == 'sms':
        send_sms(user_id, message)
    else:
        print("Unsupported notification method")