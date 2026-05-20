from typing import Dict, List

class Service:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.settings = {}

    def configure(self, settings: Dict[str, str]):
        self.settings = settings

class ServiceAPI:
    def __init__(self):
        self.services = {}

    def add_service(self, service: Service):
        self.services[service.name] = service

    def get_services(self) -> List[Service]:
        return list(self.services.values())

    def get_service(self, name: str) -> Service:
        return self.services.get(name)

    def configure_service(self, name: str, settings: Dict[str, str]):
        service = self.get_service(name)
        if service:
            service.configure(settings)