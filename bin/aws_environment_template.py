import boto3
import json

def create_aws_environment_template(template_name, template_body):
    """
    Create an AWS CloudFormation template for the practice environment.

    :param template_name: Name of the CloudFormation template
    :param template_body: JSON string representing the CloudFormation template
    """
    cloudformation = boto3.client('cloudformation')

    try:
        response = cloudformation.create_stack(
            StackName=template_name,
            TemplateBody=template_body,
            Capabilities=['CAPABILITY_IAM']
        )
        print(f"CloudFormation template {template_name} created successfully.")
        return response
    except Exception as e:
        print(f"Error creating CloudFormation template: {e}")
        raise

def generate_aws_template():
    """
    Generate a JSON template for the AWS practice environment.
    """
    template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "AWS Practice Environment Template",
        "Resources": {
            "EC2Instance": {
                "Type": "AWS::EC2::Instance",
                "Properties": {
                    "ImageId": "ami-0c55b159cbfafe1f0",
                    "InstanceType": "t2.micro",
                    "KeyName": "my-key-pair",
                    "SecurityGroupIds": ["sg-12345678"],
                    "SubnetId": "subnet-12345678",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": "PracticeEnvironment"
                        }
                    ]
                }
            },
            "S3Bucket": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": "practice-environment-bucket",
                    "AccessControl": "Private"
                }
            },
            "IAMRole": {
                "Type": "AWS::IAM::Role",
                "Properties": {
                    "AssumeRolePolicyDocument": {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": {
                                    "Service": "ec2.amazonaws.com"
                                },
                                "Action": "sts:AssumeRole"
                            }
                        ]
                    },
                    "Policies": [
                        {
                            "PolicyName": "S3Access",
                            "PolicyDocument": {
                                "Version": "2012-10-17",
                                "Statement": [
                                    {
                                        "Effect": "Allow",
                                        "Action": [
                                            "s3:GetObject",
                                            "s3:PutObject"
                                        ],
                                        "Resource": "arn:aws:s3:::practice-environment-bucket/*"
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }
    }
    return json.dumps(template)

if __name__ == "__main__":
    template_name = "AWS-Practice-Environment"
    template_body = generate_aws_template()
    create_aws_environment_template(template_name, template_body)