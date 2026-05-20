import yaml
from typing import Dict, Any

class ConversionRulesEngine:
    def __init__(self):
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict[str, Any]:
        with open('/opt/axentx/surrogate-1/src/conversion_rules/rules.yaml', 'r') as file:
            return yaml.safe_load(file)

    def convert(self, docker_compose: Dict[str, Any]) -> Dict[str, Any]:
        k8s_manifests = {}
        for service_name, service_config in docker_compose.get('services', {}).items():
            k8s_manifests[service_name] = self._convert_service(service_config)
        return k8s_manifests

    def _convert_service(self, service_config: Dict[str, Any]) -> Dict[str, Any]:
        k8s_service = {
            'apiVersion': 'v1',
            'kind': 'Service',
            'metadata': {
                'name': service_config.get('container_name', 'default-name')
            },
            'spec': {
                'ports': self._convert_ports(service_config.get('ports', [])),
                'selector': {
                    'app': service_config.get('container_name', 'default-name')
                }
            }
        }

        k8s_deployment = {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {
                'name': service_config.get('container_name', 'default-name')
            },
            'spec': {
                'replicas': service_config.get('deploy', {}).get('replicas', 1),
                'selector': {
                    'matchLabels': {
                        'app': service_config.get('container_name', 'default-name')
                    }
                },
                'template': {
                    'metadata': {
                        'labels': {
                            'app': service_config.get('container_name', 'default-name')
                        }
                    },
                    'spec': {
                        'containers': [{
                            'name': service_config.get('container_name', 'default-name'),
                            'image': service_config.get('image'),
                            'ports': self._convert_ports(service_config.get('ports', [])),
                            'env': self._convert_environment(service_config.get('environment', {}))
                        }]
                    }
                }
            }
        }

        return {
            'service': k8s_service,
            'deployment': k8s_deployment
        }

    def _convert_ports(self, ports: list) -> list:
        k8s_ports = []
        for port in ports:
            if isinstance(port, int):
                k8s_ports.append({'port': port, 'targetPort': port})
            elif isinstance(port, str):
                parts = port.split(':')
                if len(parts) == 2:
                    k8s_ports.append({'port': int(parts[0]), 'targetPort': int(parts[1])})
        return k8s_ports

    def _convert_environment(self, environment: Dict[str, Any]) -> list:
        k8s_env = []
        for key, value in environment.items():
            k8s_env.append({'name': key, 'value': str(value)})
        return k8s_env