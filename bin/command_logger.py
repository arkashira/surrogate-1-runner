import os
import json
from datetime import datetime

class CommandLogger:
    def __init__(self, log_dir='/audit_logs'):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    def log_command(self, command, user_identity, session_metadata):
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'command': command,
            'user_identity': user_identity,
            'session_metadata': session_metadata
        }
        log_file = os.path.join(self.log_dir, f"audit_log_{timestamp.replace(':', '-')}.json")
        with open(log_file, 'w') as f:
            json.dump(log_entry, f)