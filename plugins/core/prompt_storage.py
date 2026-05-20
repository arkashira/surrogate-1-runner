
import os
import json
from typing import Dict, Any

class PromptStorage:
    def __init__(self, file_path: str = 'prompt_storage.json'):
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get_prompt(self, user_id: str) -> str:
        return self.data.get(user_id, '')

    def set_prompt(self, user_id: str, prompt: str):
        self.data[user_id] = prompt
        self._save_data()

# /opt/axentx/surrogate-1/plugins/core/ai_assistance.py

from .prompt_storage import PromptStorage

class AIAssistance:
    def __init__(self):
        self.prompt_storage = PromptStorage()

    def get_custom_prompt(self, user_id: str) -> str:
        return self.prompt_storage.get_prompt(user_id)

    def set_custom_prompt(self, user_id: str, prompt: str):
        self.prompt_storage.set_prompt(user_id, prompt)

## Summary
- Added `PromptStorage` class to handle saving and loading custom prompts.
- Added `get_custom_prompt` and `set_custom_prompt` methods to `AIAssistance` class.
- Custom prompts are stored in a JSON file named `prompt_storage.json`.
- The `PromptStorage` class ensures data persistence and consistency.