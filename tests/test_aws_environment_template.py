import unittest
from unittest.mock import patch, MagicMock
import json
from bin.aws_environment_template import create_aws_environment_template, generate_aws_template

class TestAWSEvironmentTemplate(unittest.TestCase):

    @patch('boto3.client')
    def test_create_aws_environment_template_success(self, mock_boto3_client):
        mock_cloudformation = MagicMock()
        mock_boto3_client.return_value = mock_cloudformation

        template_name = "TestTemplate"
        template_body = json.dumps({"Resources": {}})

        create_aws_environment_template(template_name, template_body)

        mock_cloudformation.create_stack.assert_called_once_with(
            StackName=template_name,
            TemplateBody=template_body,
            Capabilities=['CAPABILITY_IAM']
        )

    @patch('boto3.client')
    def test_create_aws_environment_template_failure(self, mock_boto3_client):
        mock_cloudformation = MagicMock()
        mock_cloudformation.create_stack.side_effect = Exception("Test Exception")
        mock_boto3_client.return_value = mock_cloudformation

        template_name = "TestTemplate"
        template_body = json.dumps({"Resources": {}})

        with self.assertRaises(Exception) as context:
            create_aws_environment_template(template_name, template_body)

        self.assertEqual(str(context.exception), "Test Exception")

    def test_generate_aws_template(self):
        template = generate_aws_template()
        template_dict = json.loads(template)

        self.assertIn("AWSTemplateFormatVersion", template_dict)
        self.assertIn("Description", template_dict)
        self.assertIn("Resources", template_dict)
        self.assertIn("EC2Instance", template_dict["Resources"])
        self.assertIn("S3Bucket", template_dict["Resources"])
        self.assertIn("IAMRole", template_dict["Resources"])

if __name__ == '__main__':
    unittest.main()