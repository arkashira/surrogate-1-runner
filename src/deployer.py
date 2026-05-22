import os
import boto3
from botocore.exceptions import ClientError

class SurrogateDeployer:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.cloudformation = boto3.client('cloudformation')

    def deploy_environment(self, template_url, stack_name, parameters):
        try:
            response = self.cloudformation.create_stack(
                StackName=stack_name,
                TemplateURL=template_url,
                Parameters=parameters,
                Capabilities=['CAPABILITY_IAM']
            )
            return response
        except ClientError as e:
            print(f"Error deploying environment: {e}")
            raise

    def cleanup_environment(self, stack_name):
        try:
            response = self.cloudformation.delete_stack(
                StackName=stack_name
            )
            return response
        except ClientError as e:
            print(f"Error cleaning up environment: {e}")
            raise