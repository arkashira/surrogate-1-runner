import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import time

class EmailService:
    def __init__(self, smtp_config):
        self.smtp_config = smtp_config
        self.last_sent = {}

    def send_email(self, to, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_config['from']
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(self.smtp_config['host'], self.smtp_config['port'])
        server.starttls()
        server.login(self.smtp_config['username'], self.smtp_config['password'])
        text = msg.as_string()
        server.sendmail(self.smtp_config['from'], to, text)
        server.quit()

    def send_alert(self, pipeline_name, error_snippet, dashboard_link, to):
        subject = f"Pipeline {pipeline_name} failed"
        body = f"Error snippet: {error_snippet}\nDashboard link: {dashboard_link}"
        if pipeline_name not in self.last_sent or time.time() - self.last_sent[pipeline_name] > 3600:
            self.send_email(to, subject, body)
            self.last_sent[pipeline_name] = time.time()

def get_smtp_config():
    return {
        'host': os.environ['SMTP_HOST'],
        'port': int(os.environ['SMTP_PORT']),
        'username': os.environ['SMTP_USERNAME'],
        'password': os.environ['SMTP_PASSWORD'],
        'from': os.environ['SMTP_FROM']
    }