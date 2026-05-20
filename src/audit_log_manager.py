import json
import os
from datetime import datetime, timedelta
from src.audit_log import AuditLog

class AuditLogManager:
    def __init__(self, log_dir='logs', retention_days=30):
        self.log_dir = log_dir
        self.retention_days = retention_days
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def add_log(self, policy_name, result):
        log = AuditLog(policy_name, result)
        log_file = os.path.join(self.log_dir, f"{datetime.now().strftime('%Y%m%d')}.json")
        with open(log_file, 'a') as f:
            f.write(log.to_json() + '\n')

    def search_logs(self, policy_name):
        logs = []
        for log_file in os.listdir(self.log_dir):
            if log_file.endswith('.json'):
                with open(os.path.join(self.log_dir, log_file), 'r') as f:
                    for line in f:
                        log = AuditLog.from_json(line.strip())
                        if log.policy_name == policy_name:
                            logs.append(log)
        return logs

    def cleanup_old_logs(self):
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        for log_file in os.listdir(self.log_dir):
            if log_file.endswith('.json'):
                file_date = datetime.strptime(log_file.split('.')[0], '%Y%m%d')
                if file_date < cutoff:
                    os.remove(os.path.join(self.log_dir, log_file))