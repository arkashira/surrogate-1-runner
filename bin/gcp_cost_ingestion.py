import os
import json
import logging
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.cloud import storage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
BQ_DATASET_ID = os.getenv('BQ_DATASET_ID')
BQ_TABLE_ID = os.getenv('BQ_TABLE_ID')
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
GCS_BLOB_NAME = os.getenv('GCS_BLOB_NAME')

def fetch_cost_data(start_time, end_time):
    """Fetch cost data from GCP Billing Export."""
    client = bigquery.Client(project=GCP_PROJECT_ID)
    query = f"""
        SELECT *
        FROM `{GCP_PROJECT_ID}.{BQ_DATASET_ID}.{BQ_TABLE_ID}`
        WHERE usage_start_time BETWEEN '{start_time}' AND '{end_time}'
    """
    query_job = client.query(query)
    results = query_job.result()
    return [dict(row) for row in results]

def upload_to_gcs(data, bucket_name, blob_name):
    """Upload data to Google Cloud Storage."""
    storage_client = storage.Client(project=GCP_PROJECT_ID)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(json.dumps(data))
    logger.info(f"Data uploaded to gs://{bucket_name}/{blob_name}")

def main():
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=15)
    cost_data = fetch_cost_data(start_time, end_time)
    upload_to_gcs(cost_data, GCS_BUCKET_NAME, GCS_BLOB_NAME)

if __name__ == "__main__":
    main()