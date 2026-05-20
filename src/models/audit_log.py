from datetime import datetime
from typing import List

class AuditLog:
    def __init__(self, user_id: str, timestamp: datetime, action: str, change_log: str):
        self.user_id = user_id
        self.timestamp = timestamp
        self.action = action
        self.change_log = change_log

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat(),
            "action": self.action,
            "change_log": self.change_log,
        }

    @staticmethod
    def from_dict(data: dict) -> 'AuditLog':
        return AuditLog(
            user_id=data["user_id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            action=data["action"],
            change_log=data["change_log"],
        )