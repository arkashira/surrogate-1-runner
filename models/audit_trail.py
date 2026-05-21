
from datetime import datetime
from typing import List, Dict

class AuditTrail:
    def __init__(self, user_id: str, action: str, timestamp: datetime, data: Dict):
        self.user_id = user_id
        self.action = action
        self.timestamp = timestamp
        self.data = data

class AuditTrailModel:
    def __init__(self):
        self.audit_trails = []

    def create(self, user_id: str, action: str, timestamp: datetime, data: Dict):
        self.audit_trails.append(AuditTrail(user_id, action, timestamp, data))

    def get_all(self) -> List[AuditTrail]:
        return self.audit_trails