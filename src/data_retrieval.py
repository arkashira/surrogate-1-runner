import os
import json
from azure.storage.blob import BlobServiceClient

class DataRetrieval:
    def __init__(self, connection_string, container_name):
        self.connection_string = connection_string
        self.container_name = container_name
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

    def retrieve_data(self, blob_name):
        blob_client = self.container_client.get_blob_client(blob_name)
        data = blob_client.download_blob().readall()
        return json.loads(data)

# Example usage
if __name__ == "__main__":
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    container_name = "synthetic-data"
    data_retrieval = DataRetrieval(connection_string, container_name)
    blob_name = "20230505120000_5d41402abc4b2a76b9719d911017c592.json"
    data = data_retrieval.retrieve_data(blob_name)
    print(data)