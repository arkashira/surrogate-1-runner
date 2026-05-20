import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

import pika
from pydantic import BaseModel

from src.config import settings
from src.logging_system import log_alert

class Alert(BaseModel):
    severity: str
    type: str
    message: str
    timestamp: datetime

class AlertingSystem:
    def __init__(self):
        self.rabbitmq_connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
        )
        self.channel = self.rabbitmq_connection.channel()
        self.channel.queue_declare(queue='alerts', durable=True)

    def send_alert(self, alert: Alert) -> None:
        try:
            alert_dict = alert.dict()
            alert_dict['timestamp'] = alert_dict['timestamp'].isoformat()
            self.channel.basic_publish(
                exchange='',
                routing_key='alerts',
                body=json.dumps(alert_dict),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
            )
            log_alert(f"Alert sent: {alert_dict}")
        except Exception as e:
            logging.error(f"Failed to send alert: {e}")

    def close(self) -> None:
        self.rabbitmq_connection.close()

def create_alert(severity: str, alert_type: str, message: str) -> Alert:
    return Alert(
        severity=severity,
        type=alert_type,
        message=message,
        timestamp=datetime.utcnow()
    )