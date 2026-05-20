import boto3
import os
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

class AWSAuth:
    def __init__(self, role_arn=None, session_name="surrogate-1-session", region_name="us-east-1"):
        """
        Initialize AWS authentication handler.
        
        Args:
            role_arn (str): Optional IAM role ARN to assume
            session_name (str): Session name for assumed role
            region_name (str): AWS region name
        """
        self.role_arn = role_arn
        self.session_name = session_name
        self.region_name = region_name
        self.credentials = None
        self.expiry_time = None
        self.session = None
        
    def get_credentials(self):
        """
        Get AWS credentials with caching and automatic refresh.
        
        Returns:
            dict: AWS credentials (access_key, secret_key, token)
        """
        # Return cached credentials if still valid (5-minute buffer)
        if self.credentials and self.expiry_time and datetime.utcnow() < self.expiry_time - timedelta(minutes=5):
            return self.credentials
            
        try:
            if self.role_arn:
                # Assume role using STS
                sts_client = boto3.client('sts', region_name=self.region_name)
                assumed_role = sts_client.assume_role(
                    RoleArn=self.role_arn,
                    RoleSessionName=self.session_name
                )
                credentials = assumed_role['Credentials']
                self.credentials = {
                    'access_key': credentials['AccessKeyId'],
                    'secret_key': credentials['SecretAccessKey'],
                    'token': credentials['SessionToken']
                }
                self.expiry_time = credentials['Expiration'].replace(tzinfo=None)
            else:
                # Use default credential chain (EC2 metadata, env vars, etc.)
                session = boto3.Session()
                credentials = session.get_credentials()
                self.credentials = {
                    'access_key': credentials.access_key,
                    'secret_key': credentials.secret_key,
                    'token': credentials.token
                }
                # Set expiry for non-temporary credentials
                self.expiry_time = datetime.utcnow() + timedelta(hours=1)
                
            logger.info("AWS credentials refreshed successfully")
            return self.credentials
            
        except ClientError as e:
            logger.error(f"AWS authentication error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during AWS auth: {str(e)}")
            raise
            
    def get_session(self):
        """
        Get boto3 session with authenticated credentials.
        
        Returns:
            boto3.Session: Configured session
        """
        if not self.session:
            creds = self.get_credentials()
            self.session = boto3.Session(
                aws_access_key_id=creds['access_key'],
                aws_secret_access_key=creds['secret_key'],
                aws_session_token=creds['token'],
                region_name=self.region_name
            )
        return self.session
        
    def get_client(self, service_name):
        """
        Get AWS service client with authenticated session.
        
        Args:
            service_name (str): AWS service name (e.g., 's3', 'ec2')
            
        Returns:
            boto3.client: Configured service client
        """
        session = self.get_session()
        return session.client(service_name, region_name=self.region_name)

def get_aws_auth():
    """
    Factory function to create AWSAuth instance with environment configuration.
    
    Returns:
        AWSAuth: Configured authentication instance
    """
    role_arn = os.getenv('AWS_ROLE_ARN')
    region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    return AWSAuth(role_arn=role_arn, region_name=region)

# Example usage
if __name__ == "__main__":
    try:
        auth = get_aws_auth()
        s3_client = auth.get_client('s3')
        # Test connection
        s3_client.list_buckets()
        print("AWS authentication successful")
    except Exception as e:
        print(f"Authentication failed: {str(e)}")