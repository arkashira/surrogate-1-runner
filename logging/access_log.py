import logging
import json
from datetime import datetime
from typing import Dict, Any

class AccessLog:
    def __init__(self, log_file: str = 'access.log'):
        self.log_file = log_file
        logging.basicConfig(filename=self.log_file, level=logging.INFO,
                           format='%(asctime)s - %(message)s')

    def log_access(self, user: str, action: str, details: Dict[str, Any]):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user': user,
            'action': action,
            'details': details
        }
        logging.info(json.dumps(log_entry))

    def get_logs(self) -> list:
        with open(self.log_file, 'r') as f:
            logs = []
            for line in f:
                logs.append(json.loads(line.split(' - ')[1]))
            return logs