import yaml
from typing import Dict, List, Optional

class ComplianceSettings:
    def __init__(self, config_path: str = "/opt/axentx/surrogate-1/src/config/compliance_config.yaml"):
        self.config_path = config_path
        self.settings = self._load_config()

    def _load_config(self) -> Dict:
        with open(self.config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config.get('compliance', {}).get('data_residency', {})

    def get_regions(self) -> List[str]:
        return self.settings.get('regions', [])

    def get_default_region(self) -> Optional[str]:
        return self.settings.get('default_region')

    def is_enforced(self) -> bool:
        return self.settings.get('enforce', False)

    def update_settings(self, new_settings: Dict):
        self.settings.update(new_settings)
        self._save_config()

    def _save_config(self):
        with open(self.config_path, 'w') as file:
            yaml.dump({'compliance': {'data_residency': self.settings}}, file)

# Example usage
if __name__ == "__main__":
    compliance_settings = ComplianceSettings()
    print("Regions:", compliance_settings.get_regions())
    print("Default Region:", compliance_settings.get_default_region())
    print("Enforced:", compliance_settings.is_enforced())