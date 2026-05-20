import psycopg2
from datetime import datetime
from typing import Dict, Any

class AuditLogger:
    def __init__(self, db_config: Dict[str, Any]):
        self.conn = psycopg2.connect(**db_config)

    def log_download(self, ip_address: str, video_metadata: Dict[str, Any]):
        cursor = self.conn.cursor()
        query = """
        INSERT INTO audit_logs (ip_address, download_time, video_title, video_id, video_author, video_duration)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            ip_address,
            datetime.utcnow(),
            video_metadata.get('title'),
            video_metadata.get('id'),
            video_metadata.get('author'),
            video_metadata.get('duration')
        )
        cursor.execute(query, values)
        self.conn.commit()
        cursor.close()

    def close(self):
        self.conn.close()