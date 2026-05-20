import boto3
import logging
import yaml
from huggingface_hub import HfApi

logger = logging.getLogger(__name__)

def fetch_dataset_from_huggingface(config):
    api = HfApi()
    dataset_name = config['dataset_name']
    dataset_version = config['dataset_version']
    s3_bucket = config['s3_bucket']
    s3_key = config['s3_key']

    dataset_path = api.dataset_download_files(
        repo_id=dataset_name,
        revision=dataset_version,
        path=s3_key
    )

    s3 = boto3.client('s3')
    s3.upload_file(dataset_path, s3_bucket, s3_key)

    logger.info(f'Dataset uploaded to S3: {s3_bucket}/{s3_key}')

def main():
    with open('/opt/axentx/surrogate-1/config/worker.yaml', 'r') as f:
        config = yaml.safe_load(f)

    fetch_dataset_from_huggingface(config)

if __name__ == '__main__':
    main()