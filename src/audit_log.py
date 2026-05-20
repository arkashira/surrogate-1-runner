import json
from datetime import datetime

class AuditLog:
    def __init__(self, policy_name, result):
        self.timestamp = datetime.now().isoformat()
        self.policy_name = policy_name
        self.result = result

    def to_json(self):
        return json.dumps({
            'timestamp': self.timestamp,
            'policy_name': self.policy_name,
            'result': self.result
        })

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        log = AuditLog(data['policy_name'], data['result'])
        log.timestamp = data['timestamp']
        return log