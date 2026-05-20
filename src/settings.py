from src.services.sync_service import SyncService
import os

class Settings:
    def __init__(self):
        self.sync_enabled = False
        self.s3_bucket = os.getenv('S3_BUCKET')
        self.s3_key = os.getenv('S3_KEY')
        self.encryption_key = os.getenv('ENCRYPTION_KEY')
        self.sync_service = SyncService(self.s3_bucket, self.s3_key, self.encryption_key)

    def toggle_sync(self):
        self.sync_enabled = not self.sync_enabled

    def get_sync_status(self):
        if self.sync_enabled:
            return self.sync_service.get_sync_status()
        return None

    def sync_data(self, data):
        if self.sync_enabled:
            return self.sync_service.upload_to_s3(data)
        return False

    def restore_data(self):
        if self.sync_enabled:
            return self.sync_service.download_from_s3()
        return None