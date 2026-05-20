import boto3
import json
import logging
import time
from botocore.exceptions import ClientError

class AWSInventoryCollector:
    def __init__(self, account_id):
        self.account_id = account_id
        self.inventory = {}
        self.client = boto3.client('ec2')

    def collect_ec2_inventory(self):
        try:
            response = self.client.describe_instances()
            instances = response['Reservations'][0]['Instances']
            self.inventory['ec2'] = [{'id': instance['InstanceId'], 'type': instance['InstanceType']} for instance in instances]
        except ClientError as e:
            logging.error(f"Error collecting EC2 inventory: {e}")

    def collect_s3_inventory(self):
        try:
            response = self.client.list_buckets()
            buckets = response['Buckets']
            self.inventory['s3'] = [{'name': bucket['Name']} for bucket in buckets]
        except ClientError as e:
            logging.error(f"Error collecting S3 inventory: {e}")

    def collect_iam_inventory(self):
        try:
            response = self.client.list_users()
            users = response['Users']
            self.inventory['iam'] = [{'name': user['UserName']} for user in users]
        except ClientError as e:
            logging.error(f"Error collecting IAM inventory: {e}")

    def collect_rds_inventory(self):
        try:
            response = self.client.describe_db_instances()
            instances = response['DBInstances']
            self.inventory['rds'] = [{'id': instance['DBInstanceIdentifier'], 'engine': instance['Engine']} for instance in instances]
        except ClientError as e:
            logging.error(f"Error collecting RDS inventory: {e}")

    def collect_lambda_inventory(self):
        try:
            response = self.client.list_functions()
            functions = response['Functions']
            self.inventory['lambda'] = [{'name': function['FunctionName']} for function in functions]
        except ClientError as e:
            logging.error(f"Error collecting Lambda inventory: {e}")

    def collect_vpc_inventory(self):
        try:
            response = self.client.describe_vpcs()
            vpcs = response['Vpcs']
            self.inventory['vpc'] = [{'id': vpc['VpcId']} for vpc in vpcs]
        except ClientError as e:
            logging.error(f"Error collecting VPC inventory: {e}")

    def store_inventory(self):
        with open(f'/opt/axentx/surrogate-1/data/{self.account_id}/inventory.json', 'w') as f:
            json.dump(self.inventory, f)

    def run(self):
        self.collect_ec2_inventory()
        self.collect_s3_inventory()
        self.collect_iam_inventory()
        self.collect_rds_inventory()
        self.collect_lambda_inventory()
        self.collect_vpc_inventory()
        self.store_inventory()

def lambda_handler(event, context):
    account_id = context.invoked_function_arn.split(':')[4]
    collector = AWSInventoryCollector(account_id)
    collector.run()
    return {
        'statusCode': 200,
        'statusMessage': 'OK'
    }