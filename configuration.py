import json
from typing import Dict, List

class Configuration:
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

    def get_realtime_update_config(self) -> Dict:
        return self.config.get('realtime_update', {})

    def update_realtime_update_config(self, config: Dict):
        self.config['realtime_update'] = config