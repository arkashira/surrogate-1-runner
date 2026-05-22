import json
import os
from typing import Dict, Any

class UserConfig:
    def __init__(self, config_path: str = "/opt/axentx/surrogate-1/config/user_config.json"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}

    def save_config(self) -> None:
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get_model_params(self) -> Dict[str, Any]:
        return self.config.get('model_params', {})

    def set_model_params(self, temperature: float, top_p: float, max_tokens: int) -> None:
        self.config['model_params'] = {
            'temperature': temperature,
            'top_p': top_p,
            'max_tokens': max_tokens
        }
        self.save_config()

    def validate_params(self, temperature: float, top_p: float, max_tokens: int) -> bool:
        if not (0 <= temperature <= 2):
            return False
        if not (0 <= top_p <= 1):
            return False
        if max_tokens <= 0:
            return False
        return True