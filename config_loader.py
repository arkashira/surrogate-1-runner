import yaml
import os
from pydantic import BaseModel, ValidationError
from typing import List

class ServiceConfig(BaseModel):
    service_name: str
    internal_ip: str
    internal_port: int
    match_criteria: str

class ConfigLoader:
    def __init__(self, config_path='/opt/axentx/surrogate-1/config/services.yaml'):
        self.config_path = config_path
        self.services = []
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
        
        with open(self.config_path, 'r') as file:
            config_data = yaml.safe_load(file)
        
        try:
            self.services = [ServiceConfig(**service) for service in config_data.get('services', [])]
        except ValidationError as e:
            raise ValueError(f"Invalid configuration: {e}")

    def reload_config(self):
        self.load_config()
        # Logic to apply the new configuration within 5 seconds
        print("Configuration reloaded successfully.")

# Example usage
if __name__ == "__main__":
    loader = ConfigLoader()
    print(loader.services)
    loader.reload_config()