import logging
from datetime import datetime

class AuditLogger:
    def __init__(self, log_file='audit.log'):
        self.log_file = log_file
        self.logger = logging.getLogger('audit_logger')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_action(self, user_id, action, details):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"User {user_id} performed {action}. Details: {details}"
        self.logger.info(log_message)