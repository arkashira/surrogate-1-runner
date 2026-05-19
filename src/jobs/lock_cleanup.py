"""
Background job that cleans up expired locks.

Usage:
    python -m lock_cleanup          # starts the scheduler
"""

import os
import logging
from datetime import datetime, timedelta
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

# --------------------------------------------------------------------------- #
# Configuration – all values come from environment variables
# --------------------------------------------------------------------------- #
DB_URL = os.getenv("SURROGATE_DB_URL", "sqlite:///surrogate.db")  # e.g. mysql+pymysql://user:pw@host/db
LOCK_TTL_HOURS = int(os.getenv("LOCK_TTL_HOURS", "24"))          # how long a lock can live
SCHEDULE_INTERVAL_MINUTES = int(os.getenv("SCHEDULE_INTERVAL_MINUTES", "60"))  # how often to run

# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Database
# --------------------------------------------------------------------------- #
engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def get_expired_locks(session: Session) -> List[dict]:
    """
    Return a list of locks that have exceeded the TTL.

    Each lock is represented as a dict with keys:
        id, user_id, team_id, created_at, expires_at, is_locked
    """
    now = datetime.utcnow()
    ttl_delta = timedelta(hours=LOCK_TTL_HOURS)
    cutoff = now - ttl_delta

    sql = text(
        """
        SELECT id, user_id, team_id, created_at, expires_at, is_locked
        FROM locks
        WHERE created_at < :cutoff
          AND is_locked = 1
        """
    )
    result = session.execute(sql, {"cutoff": cutoff}).fetchall()
    return [dict(row) for row in result]


def release_lock(session: Session, lock: dict) -> None:
    """
    Mark the lock as released and clear its expiry timestamp.
    """
    try:
        session.execute(
            text(
                """
                UPDATE locks
                SET is_locked = 0,
                    expires_at = NULL
                WHERE id = :id
                """
            ),
            {"id": lock["id"]},
        )
        session.commit()
        logger.info(f"Lock {lock['id']} released (owner={lock['user_id']})")
    except Exception as exc:
        session.rollback()
        logger.exception(f"Failed to release lock {lock['id']}: {exc}")


def send_notification(lock: dict) -> None:
    """
    Placeholder for real notification logic.
    Replace this with an email, webhook, Slack message, etc.
    """
    message = (
        f"Lock #{lock['id']} (user {lock['user_id']}) has expired "
        f"and has been automatically released."
    )
    # Example: send_email(to=..., subject=..., body=message)
    logger.info(f"Notification sent: {message}")


def cleanup_expired_locks() -> None:
    """
    Main job entry point – fetch expired locks, release them,
    and notify the owners.
    """
    logger.info("Lock cleanup job started")
    with SessionLocal() as session:
        expired = get_expired_locks(session)
        if not expired:
            logger.info("No expired locks found")
            return

        for lock in expired:
            release_lock(session, lock)
            send_notification(lock)
    logger.info("Lock cleanup job finished")


# --------------------------------------------------------------------------- #
# Scheduler
# --------------------------------------------------------------------------- #
def start_scheduler() -> None:
    scheduler = BackgroundScheduler()
    trigger = IntervalTrigger(minutes=SCHEDULE_INTERVAL_MINUTES)
    scheduler.add_job(cleanup_expired_locks, trigger=trigger, id="lock_cleanup")
    scheduler.start()
    logger.info(
        f"Scheduler started – running every {SCHEDULE_INTERVAL_MINUTES} minutes "
        f"against DB {DB_URL}"
    )

    try:
        # Keep the main thread alive so the scheduler can run.
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped")


# --------------------------------------------------------------------------- #
# CLI entry point
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    start_scheduler()