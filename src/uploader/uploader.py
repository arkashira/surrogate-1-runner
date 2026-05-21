import os
import logging
from google.cloud import storage
from google.oauth2 import service_account

class DatasetUploader:
    """
    Handles uploading validated datasets to a Google Cloud Storage bucket.
    """
    def __init__(self, bucket_name: str, credentials_file: str):
        """
        Initializes the uploader with bucket name and credentials.

        Args:
            bucket_name (str): Name of the GCS bucket.
            credentials_file (str): Path to the service account key JSON file.
        """
        self.bucket_name = bucket_name
        self.credentials_file = credentials_file
        self.storage_client = storage.Client.from_service_account_file(
            self.credentials_file
        )
        self.bucket = self.storage_client.get_bucket(self.bucket_name)

    def upload_dataset(self, dataset_file: str):
        """
        Uploads a dataset file to the GCS bucket.

        Args:
            dataset_file (str): Path to the dataset file to upload.
        """
        blob = self.bucket.blob(os.path.basename(dataset_file))
        blob.upload_from_filename(dataset_file)
        logging.info(f"Uploaded {dataset_file} to {self.bucket_name}")

    def upload_validated_dataset(self, dataset_file: str):
        """
        Validates and uploads a dataset file.

        Args:
            dataset_file (str): Path to the validated dataset file.
        """
        # For simplicity, validation is assumed to be handled externally.
        self.upload_dataset(dataset_file)


def main():
    """
    Example usage of the DatasetUploader class.
    """
    bucket_name = "surrogate-1-storage-bucket"
    credentials_file = "/path/to/service_account_key.json"
    uploader = DatasetUploader(bucket_name, credentials_file)
    dataset_file = "/path/to/validated_dataset.csv"
    uploader.upload_validated_dataset(dataset_file)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()