import json
import os

class AuditLogConfig:
    def __init__(self, config_file='config/audit_log_config.json'):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            self.config = {'retention_days': 30}
            self.save_config()
        else:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        return self.config

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)

    def get_retention_days(self):
        return self.config.get('retention_days', 30)

    def set_retention_days(self, days):
        self.config['retention_days'] = days
        self.save_config()