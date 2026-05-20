import json
from typing import Dict, List

class Customization:
    def __init__(self):
        self.config = {}

    def load_config(self, file_path: str):
        with open(file_path, 'r') as f:
            self.config = json.load(f)

    def save_config(self, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get_workflow_config(self, workflow_id: str) -> Dict:
        return self.config.get(workflow_id, {})

    def update_workflow_config(self, workflow_id: str, config: Dict):
        self.config[workflow_id] = config

    def get_agent_config(self, agent_id: str) -> Dict:
        return self.config.get(agent_id, {})

    def update_agent_config(self, agent_id: str, config: Dict):
        self.config[agent_id] = config

    def get_customization_options(self) -> List:
        return self.config.get('customization_options', [])

    def update_customization_options(self, options: List):
        self.config['customization_options'] = options