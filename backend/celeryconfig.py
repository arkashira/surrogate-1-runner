"""
Celery configuration for the surrogate-1 backend.
"""

import os
from celery.schedules import crontab

# Broker and result backend from environment variables
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Task serialization settings
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]

# Timezone settings
timezone = "UTC"
enable_utc = True

# Beat schedule: runs nightly at 02:00 UTC
CELERY_BEAT_SCHEDULE = {
    "run-nightly-matching": {
        "task": "backend.tasks.matching.run_matching_job",
        "schedule": crontab(hour=2, minute=0),
        "options": {"queue": "matching"},
    },
}

# Default queue for all tasks
CELERY_TASK_DEFAULT_QUEUE = "default"