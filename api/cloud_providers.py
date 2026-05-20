import json
import requests

class CloudProviderAPI:
    def __init__(self, config_file):
        with open(config_file) as f:
            self.config = json.load(f)

    def connect(self, provider_name):
        config = self.config.get(provider_name)
        if not config:
            raise ValueError(f"Provider {provider_name} not found in config")

        url = config['url']
        auth = (config['username'], config['password']) if 'username' in config else None

        response = requests.get(url, auth=auth)
        response.raise_for_status()
        return response.json()

# /opt/axentx/surrogate-1/api/cloud_providers.json
{
  "aws": {
    "url": "https://aws.example.com/api/resources",
    "username": "aws_user",
    "password": "aws_password"
  },
  "google_cloud": {
    "url": "https://google_cloud.example.com/api/resources"
  }
}

## Summary
- Implemented `CloudProviderAPI` class to connect to cloud providers using their config file.
- Added `connect` method to fetch resources from the provider's API.
- Created `cloud_providers.json` file to store provider-specific configurations.