import os
import json
import logging
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Any, Optional, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationManager:
    def __init__(self):
        self.config = self._load_config()
        self.notification_channels = self._initialize_channels()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load notification configuration from environment variables."""
        config = {
            'email': {
                'enabled': os.getenv('NOTIFICATIONS_EMAIL_ENABLED', 'false').lower() == 'true',
                'smtp_server': os.getenv('NOTIFICATIONS_EMAIL_SMTP_SERVER', 'smtp.gmail.com'),
                'smtp_port': int(os.getenv('NOTIFICATIONS_EMAIL_SMTP_PORT', '587')),
                'username': os.getenv('NOTIFICATIONS_EMAIL_USERNAME', ''),
                'password': os.getenv('NOTIFICATIONS_EMAIL_PASSWORD', ''),
                'recipients': os.getenv('NOTIFICATIONS_EMAIL_RECIPIENTS', '').split(','),
            },
            'slack': {
                'enabled': os.getenv('NOTIFICATIONS_SLACK_ENABLED', 'false').lower() == 'true',
                'webhook_url': os.getenv('NOTIFICATIONS_SLACK_WEBHOOK_URL', ''),
                'channel': os.getenv('NOTIFICATIONS_SLACK_CHANNEL', '#alerts'),
            },
            'log_level': os.getenv('NOTIFICATIONS_LOG_LEVEL', 'INFO'),
        }
        return config
    
    def _initialize_channels(self) -> Dict[str, Any]:
        """Initialize notification channels based on configuration."""
        channels = {}
        
        if self.config['email']['enabled']:
            channels['email'] = EmailChannel(self.config['email'])
            
        if self.config['slack']['enabled']:
            channels['slack'] = SlackChannel(self.config['slack'])
            
        return channels
    
    def send_notification(self, title: str, message: str, container_name: str, 
                         error_details: Optional[str] = None, logs: Optional[str] = None) -> bool:
        """Send notification through all enabled channels."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        full_message = f"**Container:** {container_name}\n"
        full_message += f"**Timestamp:** {timestamp}\n\n"
        full_message += f"**Message:** {message}\n\n"
        
        if error_details:
            full_message += f"**Error Details:**\n