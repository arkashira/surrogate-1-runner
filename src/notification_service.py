import time
from datetime import datetime
from typing import Dict, Any
from .job_monitor import JobMonitor
from .notification_client import NotificationClient

class NotificationService:
    def __init__(self, job_monitor: JobMonitor, notification_client: NotificationClient):
        self.job_monitor = job_monitor
        self.notification_client = notification_client

    def monitor_jobs(self):
        """Main loop to check for failed jobs."""
        while True:
            try:
                failed_jobs = self.job_monitor.get_failed_jobs()
                print(f"Found {len(failed_jobs)}failed jobs.")
                
                for job in failed_jobs:
                    # Filter for the specific error type
                    if self._is_signature_drift(job):
                        self._process_job(job)
            except Exception as e:
                print(f"Critical error in monitor loop: {e}")
            
            # Wait before next check
            time.sleep(60)

    def _process_job(self, job: Dict[str, Any]):
        """Handles the lifecycle of a single notification."""
        try:
            # 1. Send Notification
            notification = self._build_notification(job)
            success = self.notification_client.send_notification(notification)
            
            # 2. Update Database ONLY if sending succeeded
            if success:
                self.job_monitor.mark_as_notified(job['id'])
                print(f"Job {job['id']} notified and marked.")
            else:
                print(f"Failed to notify job {job['id']}. Will retry next cycle.")

        except Exception as e:
            print(f"Error processing job {job['id']}: {e}")

    def _is_signature_drift(self, job: Dict[str, Any]) -> bool:
        return job.get('error_type') == 'signature_drift'

    def _build_notification(self, job: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'job_id': job['id'],
            'error_message': job['error_message'],
            'upstream_request': job.get('upstream_request', 'N/A'),
            'user_preferences': self._get_user_preferences(job['user_id'])
        }

    def _get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        # Placeholder for user pref lookup
        return {'notification_method': 'email', 'frequency': 'immediate'}

if __name__ == '__main__':
    # Example usage
    from src.database import Database # Assuming this exists
    db = Database() 
    monitor = JobMonitor(db)
    client = NotificationClient("http://api.example.com/notifications")
    service = NotificationService(monitor, client)
    
    print("Starting Notification Service...")
    service.monitor_jobs()