from __future__ import annotations
from celery import Celery
from .settings import settings

app = Celery("surrogate")
app.conf.broker_url = settings.broker_url
app.conf.result_backend = settings.result_backend
# Optional: enable UTC, task serialization, etc.
app.conf.timezone = "UTC"
app.conf.enable_utc = True