import requests
import logging
from datetime import datetime

class ClaudeAIModel:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.claude.ai/v1"
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        handler = logging.FileHandler('claude_integration.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def generate_request_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def query_model(self, prompt):
        url = f"{self.base_url}/complete"
        headers = self.generate_request_headers()
        payload = {
            'prompt': prompt,
            'max_tokens': 150
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            self.logger.info(f"Query successful at {datetime.now()}: {result}")
            return result['completion']
        else:
            self.logger.error(f"Error querying Claude AI: {response.text}")
            raise Exception("Failed to query Claude AI")

    def get_model_capabilities(self):
        url = f"{self.base_url}/models"
        headers = self.generate_request_headers()
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            models_info = response.json()
            self.logger.info(f"Fetched model capabilities at {datetime.now()}: {models_info}")
            return models_info
        else:
            self.logger.error(f"Error fetching model capabilities: {response.text}")
            raise Exception("Failed to fetch model capabilities")