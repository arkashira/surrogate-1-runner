import unittest
from src.conversion_rules.engine import ConversionRulesEngine

class TestConversionRulesEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ConversionRulesEngine()

    def test_convert_service(self):
        docker_compose_service = {
            'container_name': 'test-service',
            'image': 'test-image',
            'ports': ['8080:80'],
            'environment': {
                'ENV_VAR': 'value'
            }
        }

        expected_k8s_service = {
            'apiVersion': 'v1',
            'kind': 'Service',
            'metadata': {
                'name': 'test-service'
            },
            'spec': {
                'ports': [{'port': 8080, 'targetPort': 80}],
                'selector': {
                    'app': 'test-service'
                }
            }
        }

        expected_k8s_deployment = {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {
                'name': 'test-service'
            },
            'spec': {
                'replicas': 1,
                'selector': {
                    'matchLabels': {
                        'app': 'test-service'
                    }
                },
                'template': {
                    'metadata': {
                        'labels': {
                            'app': 'test-service'
                        }
                    },
                    'spec': {
                        'containers': [{
                            'name': 'test-service',
                            'image': 'test-image',
                            'ports': [{'port': 8080, 'targetPort': 80}],
                            'env': [{'name': 'ENV_VAR', 'value': 'value'}]
                        }]
                    }
                }
            }
        }

        result = self.engine._convert_service(docker_compose_service)
        self.assertEqual(result['service'], expected_k8s_service)
        self.assertEqual(result['deployment'], expected_k8s_deployment)

    def test_convert_ports(self):
        ports = ['8080:80', '9090:90']
        expected_k8s_ports = [{'port': 8080, 'targetPort': 80}, {'port': 9090, 'targetPort': 90}]
        result = self.engine._convert_ports(ports)
        self.assertEqual(result, expected_k8s_ports)

    def test_convert_environment(self):
        environment = {'ENV_VAR': 'value'}
        expected_k8s_env = [{'name': 'ENV_VAR', 'value': 'value'}]
        result = self.engine._convert_environment(environment)
        self.assertEqual(result, expected_k8s_env)

if __name__ == '__main__':
    unittest.main()