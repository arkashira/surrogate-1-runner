import logging
from typing import Dict, Any

class LoggingSystem:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('centralized_logging')

    def log_alert(self, alert_data: Dict[str, Any]) -> None:
        self.logger.info(f"Alert logged: {alert_data}")