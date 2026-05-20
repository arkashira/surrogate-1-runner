import os
import json
from datetime import datetime
from cryptography.fernet import Fernet
import boto3
from botocore.exceptions import NoCredentialsError

class SyncService:
    def __init__(self, s3_bucket, s3_key, encryption_key):
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.encryption_key = encryption_key
        self.s3_client = boto3.client('s3')

    def encrypt_data(self, data):
        fernet = Fernet(self.encryption_key)
        encrypted_data = fernet.encrypt(json.dumps(data).encode())
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        fernet = Fernet(self.encryption_key)
        decrypted_data = fernet.decrypt(encrypted_data).decode()
        return json.loads(decrypted_data)

    def upload_to_s3(self, data):
        encrypted_data = self.encrypt_data(data)
        try:
            self.s3_client.put_object(Bucket=self.s3_bucket, Key=self.s3_key, Body=encrypted_data)
            return True
        except NoCredentialsError:
            print("Credentials not available")
            return False

    def download_from_s3(self):
        try:
            response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=self.s3_key)
            encrypted_data = response['Body'].read()
            return self.decrypt_data(encrypted_data)
        except NoCredentialsError:
            print("Credentials not available")
            return None

    def get_sync_status(self):
        try:
            response = self.s3_client.head_object(Bucket=self.s3_bucket, Key=self.s3_key)
            last_modified = response['LastModified']
            size = response['ContentLength']
            return {
                'last_backup': last_modified.strftime('%Y-%m-%d %H:%M:%S'),
                'size': size
            }
        except NoCredentialsError:
            print("Credentials not available")
            return None