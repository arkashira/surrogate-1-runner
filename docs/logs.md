#!/usr/bin/env python3
"""Audit Logger for surrogate-1 process logs with enhanced features"""

import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional
import uuid
import logging

# Configuration with environment variables and defaults
WORKIO_BASE = os.environ.get("WORKIO_BASE", "/opt/axentx/surrogate-1/workio")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

class AuditLogger:
    """Enhanced audit-ready process logger with structured logging and durability"""

    def __init__(self, workflow_id: Optional[str] = None, shard_id: Optional[int] = None):
        self.workflow_id = workflow_id or os.environ.get("WORKFLOW_ID", "local")
        self.shard_id = shard_id
        self.run_uuid = str(uuid.uuid4())
        self.start_time = datetime.now(timezone.utc)
        self.events = []
        self._setup_logging()
        self._ensure_workio()

    def _setup_logging(self):
        """Configure structured logging"""
        self.logger = logging.getLogger(f"surrogate-1.{self.workflow_id}")
        self.logger.setLevel(LOG_LEVEL)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _ensure_workio(self):
        """Ensure WorkIO directory structure exists"""
        workio_path = Path(WORKIO_BASE)
        logs_dir = workio_path / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

    def _get_log_path(self) -> Path:
        """Get the log file path for this run"""
        date_str = self.start_time.strftime("%Y%m%d")
        log_dir = Path(WORKIO_BASE) / "logs" / date_str
        log_dir.mkdir(parents=True, exist_ok=True)
        filename = f"audit_{self.workflow_id}_{self.run_uuid}.jsonl"
        return log_dir / filename

    def log_event(self, event_type: str, message: str, **kwargs):
        """Log an audit event with all required fields"""
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "message": message,
            "workflow_id": self.workflow_id,
            "run_uuid": self.run_uuid,
            "shard_id": self.shard_id,
            **kwargs
        }
        self.events.append(event)
        self.logger.info(f"{event_type}: {message}")

        # Write immediately to log file for durability
        log_path = self._get_log_path()
        with open(log_path, "a") as f:
            f.write(json.dumps(event) + "\n")

    # [Previous log methods remain the same but with improved structure]

    def log_workflow_complete(self, total_records: int, total_errors: int):
        """Log workflow completion with enhanced summary"""
        end_time = datetime.now(timezone.utc)
        duration = (end_time - self.start_time).total_seconds()

        self.log_event(
            "WORKFLOW_COMPLETE",
            "Workflow complete",
            end_time=end_time.isoformat(),
            duration_seconds=duration,
            total_records=total_records,
            total_errors=total_errors
        )

        # Write comprehensive summary
        summary_path = self._get_log_path().parent / f"summary_{self.workflow_id}_{self.run_uuid}.json"
        summary = {
            "workflow_id": self.workflow_id,
            "run_uuid": self.run_uuid,
            "start_time": self.start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
            "total_records": total_records,
            "total_errors": total_errors,
            "shard_id": self.shard_id,
            "status": "COMPLETED" if total_errors == 0 else "COMPLETED_WITH_ERRORS"
        }

        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)

        self.logger.info(f"Workflow completed. Summary written to {summary_path}")

    @classmethod
    def get_logger(cls, shard_id: Optional[int] = None) -> 'AuditLogger':
        """Factory function to get an AuditLogger instance"""
        return cls(shard_id=shard_id)

if __name__ == "__main__":
    # Demo/test
    logger = AuditLogger.get_logger(shard_id=0)
    logger.log_start("test-dataset", 16)
    logger.log_shard_start(0, "abc123")
    logger.log_record_processed("rec-001", "processed", source="huggingface")
    logger.log_dedup("rec-001", "md5hash123", "store")
    logger.log_shard_complete(0, 100, 10, 90)
    logger.log_workflow_complete(100, 0)
    print(f"Log written to: {logger.get_log_path()}")