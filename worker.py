#!/usr/bin/env python3
# /opt/axentx/surrogate-1/scanner/worker.py
"""
Scanner worker that:

* Runs a scan for every registered account.
* Writes a timestamped log per account.
* Updates the registry with scan results and schedules the next run.
"""

import logging
import os
import sys
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
SCAN_INTERVAL_HOURS = 6
LOG_DIR = Path("/opt/axentx/surrogate-1/logs/scanner")
API_HOST = "0.0.0.0"
API_PORT = 8080

# Ensure log directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------- #
# Registry – thread‑safe in‑memory store
# --------------------------------------------------------------------------- #
class AccountRegistry:
    """Keeps state for each account."""
    def __init__(self):
        self._accounts: Dict[str, dict] = {}
        self._lock = logging.Lock()  # simple lock, replace with threading.Lock() if needed

    def register(self, account_id: str, name: Optional[str] = None) -> None:
        if account_id not in self._accounts:
            self._accounts[account_id] = {
                "id": account_id,
                "name": name or account_id,
                "registered_at": datetime.utcnow().isoformat(),
                "last_scan": None,
                "last_status": None,
                "last_error": None,
                "next_run": datetime.utcnow().isoformat(),
            }

    def get_all(self) -> Dict[str, dict]:
        return dict(self._accounts)

    def get(self, account_id: str) -> Optional[dict]:
        return self._accounts.get(account_id)

    def update_scan_result(self, account_id: str, status: str, error: Optional[str] = None) -> None:
        now = datetime.utcnow()
        self._accounts[account_id]["last_scan"] = now.isoformat()
        self._accounts[account_id]["last_status"] = status
        self._accounts[account_id]["last_error"] = error
        # Schedule next run
        next_run = now + timedelta(hours=SCAN_INTERVAL_HOURS)
        self._accounts[account_id]["next_run"] = next_run.isoformat()


# --------------------------------------------------------------------------- #
# Worker – executes a single scan
# --------------------------------------------------------------------------- #
class ScanWorker:
    def __init__(self, registry: AccountRegistry):
        self.registry = registry

    def _log_path(self, account_id: str) -> Path:
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return LOG_DIR / f"scan_{account_id}_{ts}.log"

    def _run_scan(self, account_id: str) -> tuple[bool, Optional[str]]:
        """Stub scan – replace with real logic."""
        log_path = self._log_path(account_id)
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger = logging.getLogger(f"scanner.{account_id}")
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)

        try:
            logger.info(f"Starting scan for account: {account_id}")
            # ---- INSERT REAL SCAN LOGIC HERE ----
            # Example: check policy violations, upload findings, etc.
            # For now we just sleep to simulate work.
            import time; time.sleep(2)
            logger.info(f"Scan completed successfully for account: {account_id}")
            return True, None
        except Exception as exc:
            err = f"Scan failed: {exc}"
            logger.error(err)
            logger.error(traceback.format_exc())
            return False, err
        finally:
            logger.removeHandler(file_handler)
            file_handler.close()

    def run_all(self) -> None:
        """Run scans for all registered accounts."""
        for account_id in self.registry.get_all():
            success, err = self._run_scan(account_id)
            status = "success" if success else "failure"
            self.registry.update_scan_result(account_id, status, err)


# --------------------------------------------------------------------------- #
# Bootstrap – register some demo accounts
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    registry = AccountRegistry()
    # In production you would load from DB / config
    for acc in ["account1", "account2", "account3"]:
        registry.register(acc)

    worker = ScanWorker(registry)
    worker.run_all()