import unittest
from unittest.mock import patch, MagicMock
from src.deployer import SurrogateDeployer

class TestSurrogateDeployer(unittest.TestCase):
    @patch('boto3.client')
    def test_deploy_environment(self, mock_boto3):
        mock_cloudformation = MagicMock()
        mock_boto3.return_value = mock_cloudformation

        deployer = SurrogateDeployer()
        template_url = 'https://example.com/template.yml'
        stack_name = 'test-stack'
        parameters = [{'ParameterKey': 'Key', 'ParameterValue': 'Value'}]

        deployer.deploy_environment(template_url, stack_name, parameters)

        mock_cloudformation.create_stack.assert_called_once_with(
            StackName=stack_name,
            TemplateURL=template_url,
            Parameters=parameters,
            Capabilities=['CAPABILITY_IAM']
        )

    @patch('boto3.client')
    def test_cleanup_environment(self, mock_boto3):
        mock_cloudformation = MagicMock()
        mock_boto3.return_value = mock_cloudformation

        deployer = SurrogateDeployer()
        stack_name = 'test-stack'

        deployer.cleanup_environment(stack_name)

        mock_cloudformation.delete_stack.assert_called_once_with(
            StackName=stack_name
        )

if __name__ == '__main__':
    unittest.main()