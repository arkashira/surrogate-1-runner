from typing import List, Dict, Any
from .database import Database

class JobMonitor:
    def __init__(self, database: Database):
        self.database = database

    def get_failed_jobs(self) -> List[Dict[str, Any]]:
        """
        Retrieves jobs that have failed and have not yet been successfully notified.
        """
        query = """
        SELECT id, error_message, upstream_request, user_id, error_type
        FROM jobs
        WHERE status = 'failed' AND notified = FALSE
        """
        return self.database.execute_query(query)

    def mark_as_notified(self, job_id: str):
        """
        Marks a specific job as notified. Called ONLY after successful delivery.
        """
        query = "UPDATE jobs SET notified = TRUE WHERE id = %s"
        self.database.execute_update(query, (job_id,))