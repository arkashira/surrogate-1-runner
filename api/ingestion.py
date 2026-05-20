import boto3
import logging
from datetime import datetime

s3 = boto3.client('s3')
logger = logging.getLogger(__name__)

def ingest_dataset(dataset_name, dataset_data):
    try:
        # Store the dataset in the configured S3 bucket with the correct key
        s3.put_object(Body=dataset_data, Bucket='axentx-datasets', Key=f'{dataset_name}.csv')
        
        # Write a success log entry to the ingestion log service
        logger.info(f'Dataset {dataset_name} ingested successfully at {datetime.now()}')
        
        return True
    except Exception as e:
        logger.error(f'Error ingesting dataset {dataset_name}: {str(e)}')
        return False