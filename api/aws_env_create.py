import boto3
import uuid
from flask import Flask, jsonify, request

app = Flask(__name__)
AWS_REGION = 'us-east-1'

@app.route('/create-aws-env', methods=['POST'])
def create_aws_environment():
    try:
        # Generate unique environment identifier
        env_id = str(uuid.uuid4())[:8]
        
        # Initialize AWS clients
        ec2 = boto3.client('ec2', region_name=AWS_REGION)
        s3 = boto3.client('s3', region_name=AWS_REGION)
        
        # Create VPC
        vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
        vpc_id = vpc['Vpc']['VpcId']
        
        # Create subnet
        subnet = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock='10.0.1.0/24'
        )
        subnet_id = subnet['Subnet']['SubnetId']
        
        # Create S3 bucket with unique name
        bucket_name = f'practice-env-bucket-{env_id}'
        s3.create_bucket(Bucket=bucket_name)
        
        # Launch EC2 instance
        instance = ec2.run_instances(
            ImageId='ami-0c55b159cbfafe1f0',  # Amazon Linux 2
            MinCount=1,
            MaxCount=1,
            SubnetId=subnet_id,
            InstanceType='t2.micro'
        )
        instance_id = instance['Instances'][0]['InstanceId']
        
        # Return environment details
        return jsonify({
            'status': 'success',
            'environment_id': env_id,
            'vpc_id': vpc_id,
            'subnet_id': subnet_id,
            'bucket_name': bucket_name,
            'instance_id': instance_id
        }), 201
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)