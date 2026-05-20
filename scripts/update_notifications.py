import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
import os
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class UpdateInfo:
    package: str
    old_version: str
    new_version: str
    timestamp: str
    environment: str

class DependencyUpdateNotifier:
    def __init__(self):
        # Configuration from environment variables with sensible defaults
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.recipients = os.getenv('NOTIFICATION_RECIPIENTS', '').split(',')

        # Validate required configuration
        if not all([self.sender_email, self.sender_password, self.recipients]):
            raise ValueError("Missing required email configuration in environment variables")

    def _create_email_message(self, update_info: UpdateInfo) -> MIMEMultipart:
        """Create formatted email message with update details"""
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = ", ".join(self.recipients)
        message["Subject"] = f"Dependency Update Successful: {update_info.package}"

        body = f"""Dependency Update Successful!

Package: {update_info.package}
Old Version: {update_info.old_version}
New Version: {update_info.new_version}
Update Time: {update_info.timestamp}
Environment: {update_info.environment}

This update was automatically applied and tested in {update_info.environment}.

Best regards,
Axentx DevOps Team
"""
        message.attach(MIMEText(body, "plain"))
        return message

    def send_notification(self, update_info: UpdateInfo) -> bool:
        """Send notification about successful dependency update"""
        try:
            message = self._create_email_message(update_info)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(
                    self.sender_email,
                    self.recipients,
                    message.as_string()
                )

            logger.info(f"Notification sent for update: {update_info.package}")
            return True

        except Exception as e:
            logger.error(f"Failed to send notification: {str(e)}")
            return False

def notify_successful_updates(dependency_updates: List[Dict[str, str]]) -> None:
    """Notify developers about successful dependency updates"""
    notifier = DependencyUpdateNotifier()

    for update in dependency_updates:
        update_info = UpdateInfo(
            package=update['package'],
            old_version=update['old_version'],
            new_version=update['new_version'],
            timestamp=update['timestamp'],
            environment=update['environment']
        )

        success = notifier.send_notification(update_info)
        if not success:
            logger.warning(f"Failed to send notification for {update['package']}")

# Example usage
if __name__ == "__main__":
    # Example update data (would come from your dependency update process)
    updates = [
        {
            'package': 'requests',
            'old_version': '2.25.1',
            'new_version': '2.28.1',
            'timestamp': '2026-05-04T10:30:00Z',
            'environment': 'staging'
        },
        {
            'package': 'numpy',
            'old_version': '1.21.0',
            'new_version': '1.22.0',
            'timestamp': '2026-05-04T10:35:00Z',
            'environment': 'staging'
        }
    ]

    notify_successful_updates(updates)