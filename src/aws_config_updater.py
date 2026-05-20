import boto3
import json
from botocore.exceptions import ClientError

class AWSConfigUpdater:
    def __init__(self, region_name='us-east-1'):
        self.region_name = region_name
        self.ec2 = boto3.client('ec2', region_name=region_name)
        self.elbv2 = boto3.client('elbv2', region_name=region_name)
        self.rds = boto3.client('rds', region_name=region_name)

    def update_ec2_instance(self, instance_id, instance_type):
        try:
            response = self.ec2.modify_instance_attribute(
                InstanceId=instance_id,
                InstanceType={'Value': instance_type}
            )
            return response
        except ClientError as e:
            print(f"Error updating EC2 instance: {e}")
            return None

    def update_load_balancer(self, load_balancer_arn, attributes):
        try:
            response = self.elbv2.modify_load_balancer_attributes(
                LoadBalancerArn=load_balancer_arn,
                Attributes=attributes
            )
            return response
        except ClientError as e:
            print(f"Error updating load balancer: {e}")
            return None

    def update_rds_instance(self, db_instance_identifier, db_instance_class):
        try:
            response = self.rds.modify_db_instance(
                DBInstanceIdentifier=db_instance_identifier,
                DBInstanceClass=db_instance_class,
                ApplyImmediately=True
            )
            return response
        except ClientError as e:
            print(f"Error updating RDS instance: {e}")
            return None

    def update_configurations(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)

        ec2_updates = config.get('ec2_instances', [])
        for update in ec2_updates:
            self.update_ec2_instance(update['instance_id'], update['instance_type'])

        elb_updates = config.get('load_balancers', [])
        for update in elb_updates:
            self.update_load_balancer(update['load_balancer_arn'], update['attributes'])

        rds_updates = config.get('rds_instances', [])
        for update in rds_updates:
            self.update_rds_instance(update['db_instance_identifier'], update['db_instance_class'])