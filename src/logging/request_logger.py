import logging
import datetime
import json
from logging.handlers import RotatingFileHandler

class RequestLogger:
    def __init__(self, log_file, max_bytes, backup_count):
        self.log_file = log_file
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.logger = logging.getLogger('request_logger')
        self.logger.setLevel(logging.INFO)
        self.handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        self.handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        self.logger.addHandler(self.handler)

    def log_request(self, user_info, request_details):
        log_message = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_info': user_info,
            'request_details': request_details
        }
        self.logger.info(json.dumps(log_message))