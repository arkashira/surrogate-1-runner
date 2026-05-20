from datetime import datetime

class Alert:
    def __init__(self, message, timestamp=None):
        self.message = message
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self):
        return {
            'message': self.message,
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['message'], datetime.fromisoformat(data['timestamp']))

    def __str__(self):
        return f"Alert: {self.message} at {self.timestamp}"