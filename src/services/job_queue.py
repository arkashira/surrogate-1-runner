import uuid
from datetime import datetime
from src.utils.database import get_db_connection

class JobQueue:
    def __init__(self):
        self.db = get_db_connection()

    def enqueue_hardening_job(self, vm_ids, policy_version):
        job_id = str(uuid.uuid4())
        created_at = datetime.utcnow()

        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO hardening_jobs (job_id, vm_ids, policy_version, status, created_at) VALUES (%s, %s, %s, %s, %s)",
            (job_id, vm_ids, policy_version, 'queued', created_at)
        )
        self.db.commit()
        cursor.close()

        return job_id

    def get_job_status(self, job_id):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT status, error_details FROM hardening_jobs WHERE job_id = %s",
            (job_id,)
        )
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        status, error_details = result
        return {
            'job_id': job_id,
            'status': status,
            'error_details': error_details
        }