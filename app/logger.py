import json
import logging
import os
from datetime import datetime
from typing import Dict, Any

class AuditLogger:
    def __init__(self, log_file: str = '/var/log/axentx/surrogate-1/audit.log'):
        self.log_file = log_file
        self.setup_logger()

    def setup_logger(self) -> None:
        """Initialize the logger with file handler and JSON formatter."""
        self.logger = logging.getLogger('audit_logger')
        self.logger.setLevel(logging.INFO)

        # Ensure log directory exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        handler = logging.FileHandler(self.log_file)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

    def log_api_request(self, request_id: str, api_key: str, endpoint: str) -> None:
        """Log an API request with structured JSON data."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'request_id': request_id,
            'api_key': api_key,
            'endpoint': endpoint
        }
        self.logger.info(json.dumps(log_entry))

    def log_custom_entry(self, data: Dict[str, Any]) -> None:
        """Log a custom structured JSON entry."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            **data
        }
        self.logger.info(json.dumps(log_entry))

# Singleton instance for easy access
audit_logger = AuditLogger()