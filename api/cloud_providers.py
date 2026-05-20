import boto3
from azure.mgmt.costmanagement import CostManagementClient
from google.cloud import billing

class CloudProviderIntegration:
    def __init__(self, provider):
        self.provider = provider
        self.client = None

    def connect(self, credentials):
        if self.provider == 'aws':
            self.client = boto3.client('ce', aws_access_key_id=credentials['access_key'], aws_secret_access_key=credentials['secret_key'])
        elif self.provider == 'azure':
            self.client = CostManagementClient(credentials, subscription_id=credentials['subscription_id'])
        elif self.provider == 'gcp':
            self.client = billing.Client(project=credentials['project_id'])

    def import_cost_data(self):
        if self.provider == 'aws':
            response = self.client.get_cost_and_usage(TimePeriod={'Start': '2023-01-01', 'End': '2023-02-01'}, Granularity='MONTHLY', Metrics=['UnblendedCost'])
            return response['ResultsByTime']
        elif self.provider == 'azure':
            query = self.client.query.create(scope='/subscriptions/{subscriptionId}', type='Usage', time_period={'from': '2023-01-01', 'to': '2023-02-01'})
            return query.as_dict()
        elif self.provider == 'gcp':
            projects = self.client.list_projects()
            costs = []
            for project in projects:
                billing_info = self.client.get_project_billing_info(name=project.name)
                costs.append({'project': project.project_id, 'billing_account': billing_info.billing_account_name})
            return costs

    def switch_provider(self, new_provider, new_credentials):
        self.provider = new_provider
        self.connect(new_credentials)

# Test cases
def test_cloud_provider_integration():
    aws_credentials = {'access_key': 'aws_access_key', 'secret_key': 'aws_secret_key'}
    azure_credentials = {'subscription_id': 'azure_subscription_id'}
    gcp_credentials = {'project_id': 'gcp_project_id'}

    aws_integration = CloudProviderIntegration('aws')
    aws_integration.connect(aws_credentials)
    aws_data = aws_integration.import_cost_data()

    azure_integration = CloudProviderIntegration('azure')
    azure_integration.connect(azure_credentials)
    azure_data = azure_integration.import_cost_data()

    gcp_integration = CloudProviderIntegration('gcp')
    gcp_integration.connect(gcp_credentials)
    gcp_data = gcp_integration.import_cost_data()

    print("AWS Data:", aws_data)
    print("Azure Data:", azure_data)
    print("GCP Data:", gcp_data)

test_cloud_provider_integration()