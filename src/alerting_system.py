import logging
from typing import Dict, Any
from .logging_system import LoggingSystem

class AlertingSystem:
    def __init__(self, logging_system: LoggingSystem):
        self.logging_system = logging_system
        self.alert_configurations = {
            'severity': ['low', 'medium', 'high', 'critical'],
            'type': ['compliance', 'security', 'performance']
        }

    def send_alert(self, alert_data: Dict[str, Any]) -> None:
        if not self._validate_alert_data(alert_data):
            logging.error("Invalid alert data")
            return

        self.logging_system.log_alert(alert_data)
        logging.info(f"Alert sent: {alert_data}")

    def _validate_alert_data(self, alert_data: Dict[str, Any]) -> bool:
        required_fields = ['severity', 'type', 'message']
        for field in required_fields:
            if field not in alert_data:
                return False
        if alert_data['severity'] not in self.alert_configurations['severity']:
            return False
        if alert_data['type'] not in self.alert_configurations['type']:
            return False
        return True