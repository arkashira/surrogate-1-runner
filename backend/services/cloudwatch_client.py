import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class CloudWatchClient:
    def __init__(self, access_key, secret_key, region_name='us-east-1'):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region_name = region_name
        self.client = None

    def _get_client(self):
        if not self.client:
            try:
                self.client = boto3.client(
                    'cloudwatch',
                    aws_access_key_id=self.access_key,
                    aws_secret_access_key=self.secret_key,
                    region_name=self.region_name
                )
            except (NoCredentialsError, PartialCredentialsError) as e:
                return None, str(e)
        return self.client, None

    def test_connection(self):
        client, error = self._get_client()
        if error:
            return {'success': False, 'message': error}

        try:
            response = client.list_metrics(MaxResults=1)
            return {'success': True, 'message': 'Connection successful'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def get_metrics(self):
        client, error = self._get_client()
        if error:
            return {'success': False, 'message': error}

        try:
            metrics = client.list_metrics()
            return {'success': True, 'metrics': metrics}
        except Exception as e:
            return {'success': False, 'message': str(e)}