
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient_email, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

# /opt/axentx/surrogate-1/src/notifications/email_notifier.py

from email_service import EmailService

def notify_about_invoice_discrepancy(discrepancy, email_service):
    subject = f"Potential Invoice Discrepancy - {discrepancy['invoice_id']}"
    body = f"We have detected a potential discrepancy in invoice {discrepancy['invoice_id']}.\n\n" \
           f"Details:\n{discrepancy['details']}\n\n" \
           f"Please review and take appropriate action."
    email_service.send_email('business_owner@example.com', subject, body)

# /opt/axentx/surrogate-1/src/invoices/discrepancies.py

def detect_discrepancies(email_service):
    # Your code to detect discrepancies goes here
    # ...

    for discrepancy in discrepancies:
        notify_about_invoice_discrepancy(discrepancy, email_service)

# /opt/axentx/surrogate-1/tests/test_email_service.py
# (Similar to Candidate 1's test_email_notification_service.py, but with EmailService)

# /opt/axentx/surrogate-1/tests/test_email_notifier.py
# (Test notify_about_invoice_discrepancy function using a mock email service)

# /opt/axentx/surrogate-1/tests/test_discrepancies.py
# (Test detect_discrepancies function with a mock email service)