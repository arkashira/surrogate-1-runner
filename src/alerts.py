import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert(email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = 'alerts@axentx.com'
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.axentx.com', 587) as server:
        server.starttls()
        server.login('alerts@axentx.com', 'password')
        server.send_message(msg)

def format_alert(vulnerability):
    subject = f"Critical Vulnerability Alert: {vulnerability['dependency']}"
    body = f"""
    Critical Vulnerability Detected:

    Dependency: {vulnerability['dependency']}
    Version: {vulnerability['version']}
    Severity: {vulnerability['severity']}
    Description: {vulnerability['description']}
    """
    return subject, body

def send_vulnerability_alert(email, vulnerability):
    subject, body = format_alert(vulnerability)
    send_alert(email, subject, body)