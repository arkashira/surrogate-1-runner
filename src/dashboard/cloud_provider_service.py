from src.cloud_providers.validator import CloudProviderValidator

class CloudProviderService:
    def __init__(self):
        self.validators = {
            'aws': CloudProviderValidator.validate_aws_credentials,
            'azure': CloudProviderValidator.validate_azure_credentials,
            'gcp': CloudProviderValidator.validate_gcp_credentials
        }

    def validate_credentials(self, provider_type, credentials):
        validator = self.validators.get(provider_type)
        if not validator:
            raise ValueError(f"Unsupported provider type: {provider_type}")

        if provider_type == 'aws':
            return validator(credentials['access_key'], credentials['secret_key'], credentials['region'])
        elif provider_type == 'azure':
            return validator(credentials['client_id'], credentials['client_secret'], credentials['tenant_id'])
        elif provider_type == 'gcp':
            return validator(credentials['service_account_info'], credentials['project_id'])