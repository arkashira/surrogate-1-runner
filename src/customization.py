from typing import Optional, Dict

class CustomizationManager:
    def __init__(self):
        self.customizations = {}

    def add_customization(self, organization_id: str, custom_settings: Dict) -> None:
        self.customizations[organization_id] = custom_settings

    def get_customization(self, organization_id: str) -> Optional[Dict]:
        return self.customizations.get(organization_id)

    def update_customization(self, organization_id: str, custom_settings: Dict) -> None:
        if organization_id in self.customizations:
            self.customizations[organization_id].update(custom_settings)
        else:
            self.add_customization(organization_id, custom_settings)