import datetime
from typing import List, Dict

_jobs: List[Dict] = [
    {
        "id": 1,
        "status": "running",
        "started_at": datetime.datetime.utcnow() - datetime.timedelta(minutes=5),
        "ended_at": None,
        "duration_seconds": None,
    },
    {
        "id": 2,
        "status": "completed",
        "started_at": datetime.datetime.utcnow() - datetime.timedelta(hours=1, minutes=10),
        "ended_at": datetime.datetime.utcnow() - datetime.timedelta(hours=1),
        "duration_seconds": 600,
    },
    {
        "id": 3,
        "status": "failed",
        "started_at": datetime.datetime.utcnow() - datetime.timedelta(hours=2),
        "ended_at": datetime.datetime.utcnow() - datetime.timedelta(hours=1, minutes=55),
        "duration_seconds": 300,
    },
]

# In production this would be dynamic (e.g., from a metrics service)
WORKER_COUNT = 16