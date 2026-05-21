#!/usr/bin/env python3
"""
Cron Scheduler for Data Ingestion Jobs
Runs the ingestion pipeline at configured intervals
"""

import schedule
import time
import subprocess
import logging
import sys
import signal
from datetime import datetime

# Configure logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/opt/axentx/surrogate-1/logs/scheduler.log')
    ]
)
logger = logging.getLogger(__name__)

# Configuration
INTERVAL_MINUTES = 30
MAIN_SCRIPT_PATH = "/opt/axentx/surrogate-1/src/main.py"


def job():
    """Execute the ingestion job with error handling"""
    logger.info("=" * 50)
    logger.info(f"Starting ingestion job at {datetime.now()}")
    
    try:
        # Use subprocess instead of os.system (better practice)
        result = subprocess.run(
            [sys.executable, MAIN_SCRIPT_PATH],
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        
        if result.returncode == 0:
            logger.info("Ingestion job completed successfully")
            if result.stdout:
                logger.info(f"Output: {result.stdout}")
        else:
            logger.error(f"Ingestion job failed with code {result.returncode}")
            if result.stderr:
                logger.error(f"Error: {result.stderr}")
                
    except subprocess.TimeoutExpired:
        logger.error("Ingestion job timed out after 1 hour")
    except Exception as e:
        logger.exception(f"Unexpected error running ingestion job: {e}")
    
    logger.info("=" * 50)


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info("Received shutdown signal, stopping scheduler...")
    sys.exit(0)


def run_scheduler():
    """Main scheduler loop"""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Schedule the job
    schedule.every(INTERVAL_MINUTES).minutes.do(job)
    
    logger.info(f"Scheduler started. Running ingestion every {INTERVAL_MINUTES} minutes")
    logger.info("Press Ctrl+C to stop")
    
    # Run once immediately on startup
    job()
    
    # Main loop
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_scheduler()