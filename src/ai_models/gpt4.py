import requests
import logging
from ai_models.base import BaseModel

class GPT4Model(BaseModel):
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url
        self.logger = logging.getLogger(__name__)

    def generate_text(self, prompt):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {'prompt': prompt}
        response = requests.post(self.api_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['text']
        else:
            self.logger.error(f'Failed to generate text: {response.text}')
            return None

    def log_access(self, user_id, prompt):
        # Log access to GPT-4
        self.logger.info(f'User {user_id} accessed GPT-4 with prompt: {prompt}')

    def get_usage_analytics(self):
        # Get usage analytics for GPT-4
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(self.api_url + '/analytics', headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            self.logger.error(f'Failed to get usage analytics: {response.text}')
            return None