import json
from datetime import datetime

class ProgressTracker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.progress_file = f"/opt/axentx/surrogate-1/data/progress_{user_id}.json"
        self.load_progress()

    def load_progress(self):
        try:
            with open(self.progress_file, 'r') as file:
                self.progress_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.progress_data = {
                'conversations': [],
                'recommendations': [],
                'last_updated': None
            }

    def save_progress(self):
        with open(self.progress_file, 'w') as file:
            json.dump(self.progress_data, file, indent=4)

    def add_conversation(self, conversation_data):
        self.progress_data['conversations'].append({
            'timestamp': datetime.now().isoformat(),
            'data': conversation_data
        })
        self.progress_data['last_updated'] = datetime.now().isoformat()
        self.save_progress()

    def add_recommendation(self, recommendation_data):
        self.progress_data['recommendations'].append({
            'timestamp': datetime.now().isoformat(),
            'data': recommendation_data
        })
        self.progress_data['last_updated'] = datetime.now().isoformat()
        self.save_progress()

    def get_progress(self):
        return self.progress_data