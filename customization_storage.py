import json
import os

class CustomizationStorage:
    def __init__(self, storage_path='/opt/axentx/surrogate-1/customization_storage.json'):
        self.storage_path = storage_path
        self.data = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.storage_path):
            return {}
        with open(self.storage_path, 'r') as f:
            return json.load(f)

    def save_data(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def set_prompt(self, key, value):
        self.data['prompts'] = self.data.get('prompts', {})
        self.data['prompts'][key] = value
        self.save_data()

    def get_prompt(self, key):
        return self.data.get('prompts', {}).get(key)

    def set_command(self, key, value):
        self.data['commands'] = self.data.get('commands', {})
        self.data['commands'][key] = value
        self.save_data()

    def get_command(self, key):
        return self.data.get('commands', {}).get(key)

    def delete_prompt(self, key):
        if 'prompts' in self.data and key in self.data['prompts']:
            del self.data['prompts'][key]
            self.save_data()

    def delete_command(self, key):
        if 'commands' in self.data and key in self.data['commands']:
            del self.data['commands'][key]
            self.save_data()