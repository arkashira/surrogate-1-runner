from __future__ import annotations

import re
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple

# ----------------------------------------------------------------------
# 1.1  Compliance Relevance
# ----------------------------------------------------------------------
class ComplianceRelevance(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"
    UNKNOWN = "unknown"

# ----------------------------------------------------------------------
# 1.2  Audit Event
# ----------------------------------------------------------------------
@dataclass
class AuditEvent:
    timestamp: str
    event_type: str
    user: Optional[str]
    action: str
    resource: Optional[str]
    status: str
    ip_address: Optional[str]
    compliance_relevance: str
    details: Dict[str, Any] = field(default_factory=dict)
    raw_line: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)