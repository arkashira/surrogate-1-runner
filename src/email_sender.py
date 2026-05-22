import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.email_template import EmailTemplate
import logging

class EmailSender:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.email_template = EmailTemplate()
        logging.basicConfig(filename='/var/log/axentx/email_delivery.log', level=logging.ERROR)

    def send_email(self, recipient_email, user_name, total_balance, mom_change):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = "Daily Account Growth Summary"

            body = self.email_template.render(user_name, total_balance, mom_change)
            msg.attach(MIMEText(body, 'html'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
        except Exception as e:
            logging.error(f"Failed to send email to {recipient_email}: {e}")