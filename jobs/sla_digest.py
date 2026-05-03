import datetime
import logging
from typing import List, Set

from axentx import db
from axentx.models import Request
from services.email_service import EmailService
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.memory import MemoryJobStore

logger = logging.getLogger(__name__)

# Define terminal statuses explicitly
TERMINAL_STATUSES: Set[str] = {"closed", "cancelled", "resolved", "rejected"}

def get_at_risk_requests() -> List[Request]:
    """Return non-terminal requests with <24h remaining."""
    return (
        db.session.query(Request)
        .filter(
            Request.time_remaining < 24 * 60 * 60,
            ~Request.status.in_(TERMINAL_STATUSES)
        )
        .all()
    )

def build_digest_email_body(requests: List[Request]) -> str:
    """Build plain-text email body with public URLs."""
    lines = ["The following requests are at risk (expiring within 24h):\n"]
    for req in requests:
        public_url = req.get_public_url()  # ensure this method exists on Request
        lines.append(f"- {req.id}: {req.title}\n  URL: {public_url}\n")
    return "".join(lines)

def run_daily_job(email_service: EmailService) -> None:
    """Idempotent daily run: one digest per owner."""
    today = datetime.date.today().isoformat()
    # Idempotency guard: skip if already run today (use cache/db in production)
    if hasattr(run_daily_job, "last_run") and run_daily_job.last_run == today:
        logger.info("SLA digest already run today. Skipping.")
        return

    at_risk = get_at_risk_requests()
    if not at_risk:
        logger.info("No at-risk requests found.")
        run_daily_job.last_run = today
        return

    # Group by owner email
    by_owner = {}
    for req in at_risk:
        owner_email = req.owner_email
        if not owner_email:
            logger.warning(f"Request {req.id} has no owner_email; skipping.")
            continue
        by_owner.setdefault(owner_email, []).append(req)

    # Send one digest per owner
    for owner_email, reqs in by_owner.items():
        subject = f"Daily SLA Digest: {len(reqs)} at-risk request(s)"
        body = build_digest_email_body(reqs)
        try:
            email_service.send_email(
                recipient_email=owner_email,
                subject=subject,
                body=body
            )
            logger.info(f"Sent digest to {owner_email} for {len(reqs)} requests.")
        except Exception as exc:
            logger.error(f"Failed to send digest to {owner_email}: {exc}")

    run_daily_job.last_run = today
    logger.info("SLA digest job completed.")

# Scheduler setup (for self-contained execution)
_scheduler = None

def start_scheduler(email_service: EmailService):
    """Start daily scheduler (runs at 00:00 UTC)."""
    global _scheduler
    if _scheduler is not None:
        return
    _scheduler = BackgroundScheduler(jobstores={"default": MemoryJobStore()})
    _scheduler.add_job(
        run_daily_job,
        trigger=CronTrigger(hour=0, minute=0),
        args=[email_service],
        id="sla_digest_daily",
        replace_existing=True
    )
    _scheduler.start()
    logger.info("SLA digest scheduler started (daily at 00:00 UTC).")

def stop_scheduler():
    global _scheduler
    if _scheduler:
        _scheduler.shutdown()
        _scheduler = None
        logger.info("SLA digest scheduler stopped.")