from dataclasses import dataclass
from typing import Dict

@dataclass
class ServiceModel:
    name: str
    description: str
    settings: Dict[str, str]

class ServiceRepository:
    def __init__(self):
        self.services = {}

    def add_service(self, service: ServiceModel):
        self.services[service.name] = service

    def get_services(self) -> List[ServiceModel]:
        return list(self.services.values())

    def get_service(self, name: str) -> ServiceModel:
        return self.services.get(name)