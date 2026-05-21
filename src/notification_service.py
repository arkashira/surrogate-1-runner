import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotificationService:
    """Service for sending email notifications via SMTP."""
    
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        sender_email: str,
        sender_password: str,
        use_tls: bool = True
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.use_tls = use_tls

    def send_notification(
        self,
        recipient_email: str,
        subject: str,
        message: str
    ) -> bool:
        """
        Send an email notification.
        
        Args:
            recipient_email: Email address of the recipient
            subject: Email subject line
            message: Email body content
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"Notification sent successfully to {recipient_email}")
            return True
            
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error sending notification: {e}")
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
        
        return False