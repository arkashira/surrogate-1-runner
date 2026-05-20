import boto3
from botocore.exceptions import ClientError

class AWSService:
    def __init__(self):
        self.client = boto3.client('cloudformation')

    def create_practice_environment(self, environment):
        stack_name = f"PracticeEnvironment-{environment.id}"
        template_body = self._get_cloudformation_template()
        
        try:
            response = self.client.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=[
                    {
                        'ParameterKey': 'EnvironmentName',
                        'ParameterValue': environment.name
                    }
                ],
                Capabilities=['CAPABILITY_IAM']
            )
            return response
        except ClientError as e:
            raise Exception(f"Failed to create AWS environment: {str(e)}")

    def _get_cloudformation_template(self):
        # Placeholder for actual CloudFormation template
        return """
        {
            "Resources": {
                "S3Bucket": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {}
                }
            }
        }
        """