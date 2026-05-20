import json
from datetime import datetime

class UserFeedbackCollector:
    def __init__(self, storage):
        self.storage = storage

    def collect_feedback(self, user_id, experience_id, feedback):
        timestamp = datetime.now().isoformat()
        feedback_data = {
            'user_id': user_id,
            'experience_id': experience_id,
            'feedback': feedback,
            'timestamp': timestamp
        }
        self.storage.store_feedback(feedback_data)

    def get_feedback(self, experience_id):
        return self.storage.retrieve_feedback(experience_id)


# Tests for user_feedback.py
def test_collect_feedback():
    mock_storage = MockStorage()
    collector = UserFeedbackCollector(mock_storage)
    collector.collect_feedback('user1', 'exp1', 'Great experience!')
    feedback = mock_storage.feedback_data[0]
    assert feedback['user_id'] == 'user1'
    assert feedback['experience_id'] == 'exp1'
    assert feedback['feedback'] == 'Great experience!'

def test_get_feedback():
    mock_storage = MockStorage()
    collector = UserFeedbackCollector(mock_storage)
    collector.collect_feedback('user1', 'exp1', 'Great experience!')
    feedback = collector.get_feedback('exp1')
    assert len(feedback) == 1
    assert feedback[0]['user_id'] == 'user1'
    assert feedback[0]['feedback'] == 'Great experience!'

class MockStorage:
    def __init__(self):
        self.feedback_data = []

    def store_feedback(self, data):
        self.feedback_data.append(data)

    def retrieve_feedback(self, experience_id):
        return [fd for fd in self.feedback_data if fd['experience_id'] == experience_id]