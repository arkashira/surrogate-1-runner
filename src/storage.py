"""Thread-safe storage for audit findings."""

import threading
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
import uuid


@dataclass
class AuditFinding:
    """Represents an audit finding with impact score."""
    finding_id: str
    policy_severity: int
    affected_resources: int
    business_value: int
    impact_score: int
    created_at: str
    updated_at: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class FindingStore:
    """Thread-safe storage for audit findings."""
    
    def __init__(self):
        self._lock = threading.RLock()
        self._findings: Dict[str, AuditFinding] = {}
    
    def add(self, finding: AuditFinding) -> AuditFinding:
        """Add a new finding to the store."""
        with self._lock:
            self._findings[finding.finding_id] = finding
            return finding
    
    def get(self, finding_id: str) -> Optional[AuditFinding]:
        """Retrieve a finding by ID."""
        with self._lock:
            return self._findings.get(finding_id)
    
    def get_all(self) -> List[AuditFinding]:
        """Retrieve all findings."""
        with self._lock:
            return list(self._findings.values())
    
    def delete(self, finding_id: str) -> bool:
        """Delete a finding by ID. Returns True if found and deleted."""
        with self._lock:
            if finding_id in self._findings:
                del self._findings[finding_id]
                return True
            return False
    
    def count(self) -> int:
        """Return the number of findings."""
        with self._lock:
            return len(self._findings)
    
    def clear(self) -> int:
        """Clear all findings. Returns count of deleted items."""
        with self._lock:
            count = len(self._findings)
            self._findings.clear()
            return count


# Global store instance
store = FindingStore()