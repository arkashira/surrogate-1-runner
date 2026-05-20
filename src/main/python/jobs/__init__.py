"""
Package initialisation for the jobs module.

Importing this module ensures that the Celery beat schedule is
registered – the task module imports `celery_app` which in turn
adds the schedule to the global `app.conf.beat_schedule`.
"""

# Import the task module so that its decorator runs.
from .pnl_daily_job import pnl_daily_job  # noqa: F401