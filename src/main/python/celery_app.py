"""
Celery application instance.

The Celery instance is created once and imported by the task module
so that the task is automatically registered.
"""

from __future__ import annotations

from celery import Celery

from .config import BROKER_URL, RESULT_BACKEND

app = Celery(
    "surrogate-1",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
)

# Optional: configure serializers, timezone, etc.
app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

# Register the beat schedule when the module is imported.
# The task module imports this file, so the schedule is added automatically.