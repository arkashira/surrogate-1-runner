import boto3
import psycopg2
from botocore.exceptions import NoCredentialsError

def get_aws_resources():
    # Initialize boto3 clients for each service
    ec2 = boto3.client('ec2')
    s3 = boto3.client('s3')
    iam = boto3.client('iam')
    rds = boto3.client('rds')
    lambda_client = boto3.client('lambda')

    # Get resources
    ec2_instances = ec2.describe_instances()
    s3_buckets = s3.list_buckets()
    iam_users = iam.list_users()
    rds_instances = rds.describe_db_instances()
    lambda_functions = lambda_client.list_functions()

    return {
        'ec2': ec2_instances['Reservations'],
        's3': s3_buckets['Buckets'],
        'iam': iam_users['Users'],
        'rds': rds_instances['DBInstances'],
        'lambda': lambda_functions['Functions']
    }

def persist_inventory(data, conn):
    cur = conn.cursor()
    for service, resources in data.items():
        for resource in resources:
            # Insert or update resource in PostgreSQL
            cur.execute(f"INSERT INTO aws_inventory.{service} ({', '.join(resource.keys())}) VALUES ({', '.join(['%s'] * len(resource))}) ON CONFLICT (id) DO UPDATE SET {', '.join([f'{k}=%s' for k in resource.keys() if k != 'id'])}", list(resource.values()))
    conn.commit()

def ingest_aws_resources():
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        data = get_aws_resources()
        persist_inventory(data, conn)
    except (Exception, psycopg2.DatabaseError, NoCredentialsError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()