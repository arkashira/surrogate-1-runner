import yaml
from typing import List, Dict, Any

class RoutingConfig:
    def __init__(self, config_path: str = "/opt/axentx/surrogate-1/config/schema.yaml"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    def get_ai_services_for_freedom_link(self) -> List[str]:
        return self.config.get('freedom_link', {}).get('ai_services', [])

    def is_freedom_link_enabled(self) -> bool:
        return self.config.get('freedom_link', {}).get('enabled', False)

class Router:
    def __init__(self):
        self.config = RoutingConfig()

    def route_request(self, service_name: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        if self._should_use_freedom_link(service_name):
            return self._route_through_freedom_link(service_name, request_data)
        return self._route_directly(service_name, request_data)

    def _should_use_freedom_link(self, service_name: str) -> bool:
        return (service_name in self.config.get_ai_services_for_freedom_link() and
                self.config.is_freedom_link_enabled())

    def _route_through_freedom_link(self, service_name: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        # Implement Freedom Link routing logic here
        return {"status": "routed_through_freedom_link", "service": service_name, "data": request_data}

    def _route_directly(self, service_name: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        # Implement direct routing logic here
        return {"status": "routed_directly", "service": service_name, "data": request_data}