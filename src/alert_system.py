from typing import Dict, List
import smtplib
from email.mime.text import MIMEText

class AlertSystem:
    def __init__(self, email_config: Dict):
        self.email_config = email_config

    def send_email_alert(self, recipient: str, subject: str, body: str) -> bool:
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.email_config['sender']
            msg['To'] = recipient

            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['username'], self.email_config['password'])
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    def send_in_app_notification(self, user_id: str, message: str) -> bool:
        # Placeholder for in-app notification logic
        print(f"Notification sent to user {user_id}: {message}")
        return True

    def send_alerts(self, recipient: str, user_id: str, discrepancies: Dict) -> bool:
        subject = "Invoice Discrepancy Alert"
        body = "The following discrepancies were detected in the invoices:\n"

        if discrepancies['duplicate']:
            body += "- Duplicate invoice detected\n"
        if discrepancies['unusual_amount']:
            body += "- Unusual amount detected\n"
        if discrepancies['missing_information']:
            body += "- Missing information detected\n"

        email_sent = self.send_email_alert(recipient, subject, body)
        notification_sent = self.send_in_app_notification(user_id, body)

        return email_sent and notification_sent