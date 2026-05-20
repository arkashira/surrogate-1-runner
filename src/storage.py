import json

class FeedbackStorage:
    def __init__(self, db_path='feedback.db'):
        self.db_path = db_path

    def store_feedback(self, feedback_data):
        with open(self.db_path, 'a') as f:
            f.write(json.dumps(feedback_data) + '\n')

    def retrieve_feedback(self, experience_id):
        feedback_list = []
        try:
            with open(self.db_path, 'r') as f:
                for line in f:
                    feedback = json.loads(line)
                    if feedback['experience_id'] == experience_id:
                        feedback_list.append(feedback)
        except FileNotFoundError:
            pass
        return feedback_list


# Tests for storage.py
def test_store_and_retrieve_feedback():
    storage = FeedbackStorage('test_feedback.db')
    feedback_data = {
        'user_id': 'user1',
        'experience_id': 'exp1',
        'feedback': 'Great experience!',
        'timestamp': '2023-10-05T14:48:00'
    }
    storage.store_feedback(feedback_data)
    retrieved_feedback = storage.retrieve_feedback('exp1')
    assert len(retrieved_feedback) == 1
    assert retrieved_feedback[0]['user_id'] == 'user1'
    assert retrieved_feedback[0]['feedback'] == 'Great experience!'