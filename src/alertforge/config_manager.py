from typing import Dict, Any
import json

class ConfigManager:
    def __init__(self):
        self.default_config_path = '/opt/axentx/surrogate-1/config/default_config.json'

    def load_default_config(self) -> Dict[str, Any]:
        """
        Load the default configuration.

        Returns:
            Dictionary containing the default configuration.
        """
        with open(self.default_config_path, 'r') as file:
            config = json.load(file)
        return config

    def save_config(self, config: Dict[str, Any], config_path: str) -> None:
        """
        Save the configuration to the specified path.

        Args:
            config: Dictionary containing the configuration to be saved.
            config_path: Path to save the configuration.
        """
        with open(config_path, 'w') as file:
            json.dump(config, file, indent=4)