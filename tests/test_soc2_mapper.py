import unittest
from unittest.mock import Mock
from soc2_mapper import Soc2Mapper

class TestSoc2Mapper(unittest.TestCase):
    def test_map_controls(self):
        terraform_config = {
            'resources': [
                {'type': 'aws_instance', 'name': 'my-instance'},
                {'type': 'aws_s3_bucket', 'name': 'my-bucket'}
            ]
        }
        helm_config = {
            'charts': [
                {'name': 'my-chart', 'version': '1.0.0'},
                {'name': 'another-chart', 'version': '2.0.0'}
            ]
        }
        mapper = Soc2Mapper(terraform_config, helm_config)
        controls = mapper.map_controls()
        self.assertEqual(len(controls), 2)
        self.assertEqual(controls[0]['control'], 'CCI-000185')
        self.assertEqual(controls[1]['control'], 'CCI-000186')

    def test_generate_documentation(self):
        terraform_config = {
            'resources': [
                {'type': 'aws_instance', 'name': 'my-instance'},
                {'type': 'aws_s3_bucket', 'name': 'my-bucket'}
            ]
        }
        helm_config = {
            'charts': [
                {'name': 'my-chart', 'version': '1.0.0'},
                {'name': 'another-chart', 'version': '2.0.0'}
            ]
        }
        mapper = Soc2Mapper(terraform_config, helm_config)
        documentation = mapper.generate_documentation()
        self.assertEqual(documentation, 'CCI-000185: Ensure AWS instance is configured with a secure password policy\nCCI-000186: Ensure Helm chart is configured with a secure secret policy\n')

    def test_sign_documentation(self):
        terraform_config = {
            'resources': [
                {'type': 'aws_instance', 'name': 'my-instance'},
                {'type': 'aws_s3_bucket', 'name': 'my-bucket'}
            ]
        }
        helm_config = {
            'charts': [
                {'name': 'my-chart', 'version': '1.0.0'},
                {'name': 'another-chart', 'version': '2.0.0'}
            ]
        }
        mapper = Soc2Mapper(terraform_config, helm_config)
        signature = mapper.sign_documentation()
        self.assertEqual(signature, hashlib.sha256(mapper.generate_documentation().encode()).hexdigest())

    def test_create_pdf(self):
        terraform_config = {
            'resources': [
                {'type': 'aws_instance', 'name': 'my-instance'},
                {'type': 'aws_s3_bucket', 'name': 'my-bucket'}
            ]
        }
        helm_config = {
            'charts': [
                {'name': 'my-chart', 'version': '1.0.0'},
                {'name': 'another-chart', 'version': '2.0.0'}
            ]
        }
        mapper = Soc2Mapper(terraform_config, helm_config)
        pdf = mapper.create_pdf()
        self.assertEqual(pdf, 'Signed SOC 2 documentation: CCI-000185: Ensure AWS instance is configured with a secure password policy\nCCI-000186: Ensure Helm chart is configured with a secure secret policy\n 2a0a4b7c7d7e7f7g7h7i7j7k7l7m7n7o7p7q7r7s7t7u7v7w7x7y7z7')

if __name__ == '__main__':
    unittest.main()