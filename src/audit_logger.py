import json
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

class AuditLogger:
    def __init__(self):
        self.logger = logging.getLogger('audit_logger')
        self.logger.setLevel(logging.INFO)

        # Configure rotating file handler with proper retention policy
        handler = RotatingFileHandler(
            '/var/log/surrogate-1/audit.log',
            maxBytes=1024*1024,  # 1MB per file
            backupCount=90      # Keep 90 days of logs (90 files)
        )
        
        # Use JSON formatter for structured logging
        formatter = logging.Formatter(
            '%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)

    def log_request(self, request_id, user_id, model, endpoint, tunnel_used, response_status):
        """Log a structured request entry as JSON"""
        log_entry = {
            'request_id': request_id,
            'user_id': user_id,
            'model': model,
            'endpoint': endpoint,
            'tunnel_used': tunnel_used,
            'timestamp': datetime.utcnow().isoformat(),
            'response_status': response_status
        }
        self.logger.info(json.dumps(log_entry))