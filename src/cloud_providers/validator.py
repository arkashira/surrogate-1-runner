import boto3
from azure.identity import DefaultAzureCredential
from google.cloud import storage
from google.oauth2 import service_account

class CloudProviderValidator:
    @staticmethod
    def validate_aws_credentials(access_key, secret_key, region):
        try:
            session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )
            sts = session.client('sts')
            sts.get_caller_identity()
            return True
        except Exception as e:
            print(f"AWS credential validation failed: {e}")
            return False

    @staticmethod
    def validate_azure_credentials(client_id, client_secret, tenant_id):
        try:
            credential = DefaultAzureCredential(
                client_id=client_id,
                client_secret=client_secret,
                tenant_id=tenant_id
            )
            credential.get_token("https://management.azure.com/.default")
            return True
        except Exception as e:
            print(f"Azure credential validation failed: {e}")
            return False

    @staticmethod
    def validate_gcp_credentials(service_account_info, project_id):
        try:
            credentials = service_account.Credentials.from_service_account_info(service_account_info)
            client = storage.Client(credentials=credentials, project=project_id)
            client.list_buckets()
            return True
        except Exception as e:
            print(f"GCP credential validation failed: {e}")
            return False