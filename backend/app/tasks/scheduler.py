from celery import shared_task
from celery.beat import Scheduler
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from .models import RecordingJob

logger = get_task_logger(__name__)

@shared_task
def schedule_recording():
    # Get all scheduled recording jobs
    jobs = RecordingJob.objects.filter(status='scheduled')
    
    # Iterate over each job
    for job in jobs:
        # Check if the job's start time is now or in the past
        if job.start_time <= datetime.now():
            # Start the recording
            start_recording.apply_async(args=[job.id])
            
            # Update the job's status
            job.status = 'in_progress'
            job.save()
            
        # Check if the job's end time is now or in the past
        if job.end_time <= datetime.now():
            # Stop the recording
            stop_recording.apply_async(args=[job.id])
            
            # Update the job's status
            job.status = 'completed'
            job.save()

@shared_task
def start_recording(job_id):
    # Get the recording job
    job = RecordingJob.objects.get(id=job_id)
    
    # Start the recording
    # This is a placeholder for the actual recording code
    logger.info(f'Starting recording for job {job_id}')

@shared_task
def stop_recording(job_id):
    # Get the recording job
    job = RecordingJob.objects.get(id=job_id)
    
    # Stop the recording
    # This is a placeholder for the actual recording code
    logger.info(f'Stopping recording for job {job_id}')

class RecordingScheduler(Scheduler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schedule = {
            'schedule-recording': {
                'task': 'scheduler.schedule_recording',
                'schedule': timedelta(minutes=1),  # Run every minute
            },
        }