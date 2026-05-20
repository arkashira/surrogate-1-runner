import logging
from typing import Dict, List
import smtplib
from email.mime.text import MIMEText

class NotificationSystem:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def log_error(self, error: str, error_type: str):
        self.logger.error(f"Error Type: {error_type}, Error: {error}")

    def send_notification(self, error: str, error_type: str):
        if error_type in self.config.get('critical_errors', []):
            self._send_email_notification(error, error_type)

    def _send_email_notification(self, error: str, error_type: str):
        msg = MIMEText(f"Error Type: {error_type}\nError: {error}")
        msg['Subject'] = f"Critical Error Notification: {error_type}"
        msg['From'] = self.config.get('email_from')
        msg['To'] = self.config.get('email_to')

        try:
            with smtplib.SMTP(self.config.get('smtp_server'), self.config.get('smtp_port')) as server:
                server.starttls()
                server.login(self.config.get('smtp_username'), self.config.get('smtp_password'))
                server.send_message(msg)
            self.logger.info("Notification email sent successfully")
        except Exception as e:
            self.logger.error(f"Failed to send notification email: {e}")

# Example usage
if __name__ == "__main__":
    config = {
        'critical_errors': ['database_connection_error', 'api_failure'],
        'email_from': 'notifications@example.com',
        'email_to': 'platform_engineer@example.com',
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587,
        'smtp_username': 'username',
        'smtp_password': 'password'
    }
    notification_system = NotificationSystem(config)
    notification_system.log_error("Failed to connect to database", "database_connection_error")
    notification_system.send_notification("Failed to connect to database", "database_connection_error")