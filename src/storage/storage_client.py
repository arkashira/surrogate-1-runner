import os
import logging
from google.cloud import storage
from google.oauth2 import service_account

class StorageClient:
    """
    Manages interactions with a Google Cloud Storage bucket.
    """
    def __init__(self, bucket_name: str, credentials_file: str):
        """
        Initializes the storage client with bucket name and credentials.

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

    def get_bucket(self):
        """
        Returns the bucket object.

        Returns:
            storage.Bucket: The GCS bucket object.
        """
        return self.bucket

    def upload_file(self, file_path: str):
        """
        Uploads a file to the GCS bucket.

        Args:
            file_path (str): Path to the file to upload.
        """
        blob = self.bucket.blob(os.path.basename(file_path))
        blob.upload_from_filename(file_path)
        logging.info(f"Uploaded {file_path} to {self.bucket_name}")

    def download_file(self, file_name: str, download_path: str):
        """
        Downloads a file from the GCS bucket.

        Args:
            file_name (str): Name of the file to download.
            download_path (str): Path to save the downloaded file.
        """
        blob = self.bucket.blob(file_name)
        blob.download_to_filename(download_path)
        logging.info(f"Downloaded {file_name} from {self.bucket_name} to {download_path}")


def main():
    """
    Example usage of the StorageClient class.
    """
    bucket_name = "surrogate-1-storage-bucket"
    credentials_file = "/path/to/service_account_key.json"
    storage_client = StorageClient(bucket_name, credentials_file)
    file_path = "/path/to/file.csv"
    storage_client.upload_file(file_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()