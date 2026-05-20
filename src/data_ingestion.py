import os
import hashlib
import json
from datetime import datetime
from azure.storage.blob import BlobServiceClient

class DataIngestion:
    def __init__(self, connection_string, container_name):
        self.connection_string = connection_string
        self.container_name = container_name
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

    def generate_md5_hash(self, data):
        return hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()

    def upload_data(self, data, blob_name):
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.upload_blob(json.dumps(data), overwrite=True)

    def ingest_data(self, data):
        md5_hash = self.generate_md5_hash(data)
        blob_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{md5_hash}.json"
        self.upload_data(data, blob_name)
        return blob_name

# Example usage
if __name__ == "__main__":
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    container_name = "synthetic-data"
    data_ingestion = DataIngestion(connection_string, container_name)
    sample_data = {"key": "value"}
    blob_name = data_ingestion.ingest_data(sample_data)
    print(f"Data ingested and stored as {blob_name}")