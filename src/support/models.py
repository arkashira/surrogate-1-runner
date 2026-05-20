from datetime import datetime

class SupportRequest:
    def __init__(self, issue, status='open'):
        self.id = None
        self.issue = issue
        self.status = status
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'issue': self.issue,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Feedback:
    def __init__(self, feedback):
        self.id = None
        self.feedback = feedback
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'feedback': self.feedback,
            'created_at': self.created_at
        }