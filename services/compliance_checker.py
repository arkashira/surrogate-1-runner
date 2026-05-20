import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class ComplianceRule(Enum):
    DATA_PRIVACY = "data_privacy"
    SOURCE_APPROVAL = "source_approval"
    DATA_LICENSE = "data_license"
    CONTENT_MODERATION = "content_moderation"


class ComplianceStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"


class ComplianceCheckResult:
    def __init__(self, rule: ComplianceRule, status: ComplianceStatus, 
                 details: Dict, timestamp: datetime):
        self.rule = rule
        self.status = status
        self.details = details
        self.timestamp = timestamp
    
    def to_dict(self) -> Dict:
        return {
            "rule": self.rule.value,
            "status": self.status.value,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }


class ComplianceChecker:
    """Real-time compliance checker for AI operations."""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self._approved_sources = self.config.get("approved_sources", [])
        self._audit_log = []
    
    def check_data_privacy(self, training_data: Dict) -> ComplianceCheckResult:
        """Verify training data is from approved sources and meets privacy requirements."""
        result = {
            "source_verified": False,
            "pii_detected": False,
            "anonymization_level": "unknown"
        }
        
        # Check if source is approved
        source = training_data.get("source")
        if source in self._approved_sources:
            result["source_verified"] = True
        
        # Check for PII indicators
        if training_data.get("pii_detected", False):
            result["pii_detected"] = True
            result["anonymization_level"] = training_data.get("anonymization_level", "none")
        
        status = ComplianceStatus.FAIL
        if result["source_verified"] and not result["pii_detected"]:
            status = ComplianceStatus.PASS
        elif result["source_verified"] and result["pii_detected"] and result["anonymization_level"] == "high":
            status = ComplianceStatus.WARNING
        
        return ComplianceCheckResult(
            rule=ComplianceRule.DATA_PRIVACY,
            status=status,
            details=result,
            timestamp=datetime.utcnow()
        )
    
    def check_source_approval(self, source: str) -> ComplianceCheckResult:
        """Verify training source is in approved list."""
        is_approved = source in self._approved_sources
        
        return ComplianceCheckResult(
            rule=ComplianceRule.SOURCE_APPROVAL,
            status=ComplianceStatus.PASS if is_approved else ComplianceStatus.FAIL,
            details={"source": source, "is_approved": is_approved},
            timestamp=datetime.utcnow()
        )
    
    def check_data_license(self, license: str) -> ComplianceCheckResult:
        """Verify data license allows training use."""
        allowed_licenses = {"cc-by-4.0", "cc-by-sa-4.0", "mit", "apache-2.0", "public-domain"}
        is_allowed = license.lower() in allowed_licenses
        
        return ComplianceCheckResult(
            rule=ComplianceRule.DATA_LICENSE,
            status=ComplianceStatus.PASS if is_allowed else ComplianceStatus.FAIL,
            details={"license": license, "is_allowed": is_allowed},
            timestamp=datetime.utcnow()
        )
    
    def run_full_check(self, training_data: Dict) -> List[ComplianceCheckResult]:
        """Run all compliance checks on training data."""
        results = []
        
        results.append(self.check_data_privacy(training_data))
        results.append(self.check_source_approval(training_data.get("source", "")))
        results.append(self.check_data_license(training_data.get("license", "")))
        
        return results
    
    def log_to_audit(self, result: ComplianceCheckResult):
        """Log compliance check result to audit trail."""
        log_entry = {
            "event_type": "compliance_check",
            "rule": result.rule.value,
            "status": result.status.value,
            "details": result.details,
            "timestamp": result.timestamp.isoformat(),
            "check_hash": hashlib.md5(json.dumps(result.to_dict(), sort_keys=True).encode()).hexdigest()
        }
        self._audit_log.append(log_entry)
        logger.info(f"Compliance check logged: {log_entry}")
    
    def get_audit_log(self) -> List[Dict]:
        """Retrieve audit log entries."""
        return self._audit_log.copy()
    
    def clear_audit_log(self):
        """Clear audit log for testing purposes."""
        self._audit_log.clear()
        logger.info("Audit log cleared")


# Singleton instance for service-wide use
_compliance_checker = None

def get_compliance_checker() -> ComplianceChecker:
    """Get or create the global compliance checker instance."""
    global _compliance_checker
    if _compliance_checker is None:
        _compliance_checker = ComplianceChecker()
    return _compliance_checker