import unittest
from unittest.mock import patch, MagicMock
from src.api import app

class TestAPI(unittest.TestCase):
    @patch('src.api.SurrogateDeployer')
    def test_deploy(self, mock_deployer):
        mock_deployer_instance = MagicMock()
        mock_deployer.return_value = mock_deployer_instance
        mock_deployer_instance.deploy_environment.return_value = {'StackId': 'test-stack-id'}

        app.testing = True
        client = app.test_client()

        response = client.post('/deploy', json={
            'template_url': 'https://example.com/template.yml',
            'stack_name': 'test-stack',
            'parameters': [{'ParameterKey': 'Key', 'ParameterValue': 'Value'}]
        })

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json, {'message': 'Deployment started', 'stack_id': 'test-stack-id'})

    @patch('src.api.SurrogateDeployer')
    def test_cleanup(self, mock_deployer):
        mock_deployer_instance = MagicMock()
        mock_deployer.return_value = mock_deployer_instance
        mock_deployer_instance.cleanup_environment.return_value = {'StackId': 'test-stack-id'}

        app.testing = True
        client = app.test_client()

        response = client.post('/cleanup', json={
            'stack_name': 'test-stack'
        })

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json, {'message': 'Cleanup started', 'stack_id': 'test-stack-id'})

if __name__ == '__main__':
    unittest.main()