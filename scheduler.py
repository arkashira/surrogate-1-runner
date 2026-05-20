"""
Scheduler for surrogate-1.

This module sets up a background scheduler that triggers the weekly
marketing plan generation job every Monday at 00:00 UTC. The job
calls `generate_marketing_plan`, which is a placeholder for the
actual plan generation logic (emailing the founder and updating the
dashboard). The scheduler is started automatically when this module
is imported, making it suitable for deployment in a long‑running
service or a container entrypoint.

Dependencies:
    - APScheduler (pip install APScheduler)
"""

from datetime import datetime, time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from typing import List, Dict

# Configure module level logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ----------------------------------------------------------------------
# Placeholder for the actual marketing plan generation logic.
# ----------------------------------------------------------------------
def generate_marketing_plan() -> Dict[str, List[Dict]]:
    """
    Generate a weekly marketing plan.

    Returns:
        A dictionary containing the plan details. The structure is
        expected to be:
            {
                "date": "YYYY-MM-DD",
                "items": [
                    {
                        "description": str,
                        "expected_impact": str,
                        "checklist": List[str]
                    },
                    ...
                ]
            }

    Note:
        The real implementation would create actionable items,
        send an email to the founder, and persist the plan to the
        dashboard database. For the purposes of this scheduler,
        we return a mock plan.
    """
    today = datetime.utcnow().date()
    plan = {
        "date": today.isoformat(),
        "items": [
            {
                "description": "Optimize landing page headline",
                "expected_impact": "Increase click‑through rate by ~5%",
                "checklist": [
                    "Draft new headline variants",
                    "Run A/B test on 2 variants",
                    "Analyze results and implement winner"
                ]
            },
            {
                "description": "Publish blog post on emerging AI trends",
                "expected_impact": "Drive 10% more organic traffic",
                "checklist": [
                    "Outline article structure",
                    "Write content (≈800 words)",
                    "Add internal and external links",
                    "Schedule publication for Wednesday"
                ]
            },
            {
                "description": "Reach out to 3 industry influencers for collaboration",
                "expected_impact": "Generate 2 new backlinks",
                "checklist": [
                    "Identify target influencers",
                    "Craft personalized outreach emails",
                    "Track responses and follow‑ups"
                ]
            }
        ]
    }
    logger.info("Generated marketing plan for %s", plan["date"])
    # TODO: Email founder and persist plan to dashboard
    return plan

# ----------------------------------------------------------------------
# Scheduler setup
# ----------------------------------------------------------------------
def _setup_scheduler() -> BackgroundScheduler:
    """
    Create and configure a BackgroundScheduler instance.

    Returns:
        Configured BackgroundScheduler.
    """
    scheduler = BackgroundScheduler(timezone="UTC")
    # Add a weekly job that runs every Monday at 00:00 UTC
    trigger = CronTrigger(day_of_week="mon", hour=0, minute=0)
    scheduler.add_job(
        generate_marketing_plan,
        trigger=trigger,
        id="weekly_marketing_plan",
        name="Generate weekly marketing plan",
        replace_existing=True,
    )
    logger.info("Scheduled weekly marketing plan job for Monday 00:00 UTC")
    return scheduler

# Instantiate and start the scheduler when this module is imported
scheduler = _setup_scheduler()
scheduler.start()
logger.info("Marketing plan scheduler started")

# ----------------------------------------------------------------------
# Expose a function to manually trigger the job (useful for tests)
# ----------------------------------------------------------------------
def run_marketing_plan_now() -> Dict:
    """
    Manually trigger the marketing plan generation.

    Returns:
        The plan dictionary returned by `generate_marketing_plan`.
    """
    return generate_marketing_plan()