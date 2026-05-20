
import logging
from typing import Any, Dict, List, Union
import time

from surrogate_1.error_handling import ErrorHandler
from surrogate_1.workflow import WorkflowInstance

class Debugger:
    def __init__(self, instance: WorkflowInstance):
        self.instance = instance
        self.error_handler = ErrorHandler(instance)
        self.logger = logging.getLogger(__name__)

    def start(self):
        self.instance.start()
        self.monitor_instance()

    def monitor_instance(self):
        while True:
            try:
                logging.info(f"Monitoring workflow instance {self.instance.id}...")
                time.sleep(1)  # Simulate real-time monitoring
                for event in self.instance.events:
                    if event["type"] == "error":
                        self.handle_error(event)
            except Exception as e:
                self.logger.error(f"Error monitoring workflow instance {self.instance.id}: {str(e)}")

    def handle_error(self, event: Dict[str, Any]):
        error_data = event["data"]
        self.error_handler.log_error(error_data)
        self.error_handler.trigger_alert(error_data)

# src/error_handling.py

import logging
import smtplib
from email.mime.text import MIMEText

class ErrorHandler:
    def __init__(self, instance: WorkflowInstance):
        self.instance = instance
        self.logger = logging.getLogger(__name__)
        self.email_config = {
            "email": "error_alerts@axentx.com",
            "password": "secret_password",
            "recipient": "ai_ml_engineer@axentx.com",
        }

    def log_error(self, error_data: Dict[str, Any]):
        self.logger.error(f"Error occurred in workflow instance {self.instance.id}: {error_data}")

    def trigger_alert(self, error_data: Dict[str, Any]):
        try:
            self.send_email(f"Error in workflow instance {self.instance.id}", error_data)
        except Exception as e:
            self.logger.error(f"Error triggering alert for workflow instance {self.instance.id}: {str(e)}")

    def send_email(self, subject: str, body: str):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.email_config["email"]
        msg["To"] = self.email_config["recipient"]

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.email_config["email"], self.email_config["password"])
            server.send_message(msg)