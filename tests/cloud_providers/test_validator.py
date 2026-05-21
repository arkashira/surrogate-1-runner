import unittest
from unittest.mock import patch, MagicMock
from src.cloud_providers.validator import CloudProviderValidator

class TestCloudProviderValidator(unittest.TestCase):
    @patch('boto3.Session')
    def test_validate_aws_credentials(self, mock_session):
        mock_sts = MagicMock()
        mock_session.return_value.client.return_value = mock_sts
        mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}

        result = CloudProviderValidator.validate_aws_credentials('access_key', 'secret_key', 'us-east-1')
        self.assertTrue(result)

    @patch('azure.identity.DefaultAzureCredential')
    def test_validate_azure_credentials(self, mock_credential):
        mock_credential.return_value.get_token.return_value = {'token': 'fake_token'}

        result = CloudProviderValidator.validate_azure_credentials('client_id', 'client_secret', 'tenant_id')
        self.assertTrue(result)

    @patch('google.cloud.storage.Client')
    def test_validate_gcp_credentials(self, mock_client):
        mock_client.return_value.list_buckets.return_value = []

        service_account_info = {
            "type": "service_account",
            "project_id": "project_id",
            "private_key_id": "private_key_id",
            "private_key": "private_key",
            "client_email": "client_email",
            "client_id": "client_id",
            "auth_uri": "auth_uri",
            "token_uri": "token_uri",
            "auth_provider_x509_cert_url": "auth_provider_x509_cert_url",
            "client_x509_cert_url": "client_x509_cert_url"
        }

        result = CloudProviderValidator.validate_gcp_credentials(service_account_info, 'project_id')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()