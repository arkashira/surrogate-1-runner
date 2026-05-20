import boto3
import botocore
import sys
import os

def validate_neptune_connectivity():
    aws_region = os.getenv('AWS_REGION')
    neptune_endpoint = os.getenv('NEPTUNE_ENDPOINT')

    if not aws_region or not neptune_endpoint:
        print("Error: AWS_REGION and NEPTUNE_ENDPOINT environment variables must be set.")
        sys.exit(1)

    try:
        # Create a Neptune client
        neptune_client = boto3.client('neptune', region_name=aws_region)

        # Describe the DB instance to check connectivity
        neptune_client.describe_db_instances(DBInstanceIdentifier=neptune_endpoint)

        print("Successfully connected to AWS Neptune endpoint: " + neptune_endpoint)
        sys.exit(0)

    except botocore.exceptions.ClientError as e:
        print("Error connecting to AWS Neptune: " + str(e))
        sys.exit(1)
    except botocore.exceptions.BotoCoreError as e:
        print("Error connecting to AWS Neptune: " + str(e))
        sys.exit(1)

if __name__ == "__main__":
    validate_neptune_connectivity()