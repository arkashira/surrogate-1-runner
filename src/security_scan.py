import boto3
from botocore.exceptions import ClientError

class SecurityScanner:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.s3 = boto3.client('s3')

    def scan_ec2_instances(self):
        try:
            response = self.ec2.describe_instances()
            instances = response['Reservations']
            vulnerabilities = []

            for reservation in instances:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    # Check for vulnerabilities in the instance
                    # This is a placeholder for actual security checks
                    if self._has_vulnerabilities(instance):
                        vulnerabilities.append({
                            'InstanceId': instance_id,
                            'Vulnerabilities': self._get_vulnerabilities(instance)
                        })

            return vulnerabilities
        except ClientError as e:
            print(f"Error scanning EC2 instances: {e}")
            return []

    def scan_s3_buckets(self):
        try:
            response = self.s3.list_buckets()
            buckets = response['Buckets']
            vulnerabilities = []

            for bucket in buckets:
                bucket_name = bucket['Name']
                # Check for vulnerabilities in the bucket
                # This is a placeholder for actual security checks
                if self._has_vulnerabilities(bucket):
                    vulnerabilities.append({
                        'BucketName': bucket_name,
                        'Vulnerabilities': self._get_vulnerabilities(bucket)
                    })

            return vulnerabilities
        except ClientError as e:
            print(f"Error scanning S3 buckets: {e}")
            return []

    def _has_vulnerabilities(self, resource):
        # Placeholder for actual vulnerability detection logic
        return True

    def _get_vulnerabilities(self, resource):
        # Placeholder for actual vulnerability details
        return ["Example vulnerability"]

    def run_security_scan(self):
        ec2_vulnerabilities = self.scan_ec2_instances()
        s3_vulnerabilities = self.scan_s3_buckets()

        return {
            'EC2Instances': ec2_vulnerabilities,
            'S3Buckets': s3_vulnerabilities
        }