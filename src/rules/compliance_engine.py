from typing import Dict, List, Tuple
import datetime
import re

class ComplianceRuleEngine:
    def __init__(self):
        self.rules = [
            self._rule_phi_identifiers,
            self._rule_encryption_check,
            self._rule_audit_logging,
            self._rule_access_controls,
            self._rule_data_integrity,
            self._rule_access_security,
            self._rule_change_management,
            self._rule_monitoring
        ]

    def scan_record(self, record: Dict) -> List[Tuple[str, bool, str]]:
        """Scan a single record for compliance"""
        results = []
        for rule in self.rules:
            rule_name, compliant, message = rule(record)
            results.append((rule_name, compliant, message))
        return results

    def _rule_phi_identifiers(self, record: Dict) -> Tuple[str, bool, str]:
        """Check for Protected Health Information (PHI) identifiers"""
        phi_patterns = [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b\d{10}\b',              # Phone numbers
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b\d{3}-\d{3}-\d{4}\b'    # Medical record numbers
        ]

        for key, value in record.items():
            if isinstance(value, str):
                for pattern in phi_patterns:
                    if re.search(pattern, value):
                        return ("PHI Identifiers", False, f"Potential PHI found in {key}: {value}")
        return ("PHI Identifiers", True, "No PHI identifiers detected")

    def _rule_encryption_check(self, record: Dict) -> Tuple[str, bool, str]:
        """Verify sensitive data is encrypted"""
        sensitive_fields = ['ssn', 'medical_record', 'diagnosis', 'treatment']

        for field in sensitive_fields:
            if field in record and not record[field].startswith('ENC:'):
                return ("Encryption", False, f"Unencrypted sensitive data in {field}")
        return ("Encryption", True, "Sensitive fields properly encrypted")

    def _rule_audit_logging(self, record: Dict) -> Tuple[str, bool, str]:
        """Ensure audit trails exist for access/modification"""
        if 'access_log' not in record or 'modification_log' not in record:
            return ("Audit Logging", False, "Missing audit trail fields")
        return ("Audit Logging", True, "Audit trails present")

    def _rule_access_controls(self, record: Dict) -> Tuple[str, bool, str]:
        """Validate access control mechanisms"""
        if 'access_level' not in record:
            return ("Access Controls", False, "Missing access level specification")

        valid_levels = ['admin', 'provider', 'patient', 'system']
        if record['access_level'] not in valid_levels:
            return ("Access Controls", False, f"Invalid access level: {record['access_level']}")
        return ("Access Controls", True, "Valid access controls implemented")

    def _rule_data_integrity(self, record: Dict) -> Tuple[str, bool, str]:
        """Verify data integrity through checksums and timestamps"""
        if 'checksum' not in record:
            return ("Data Integrity", False, "Missing data checksum")

        if 'last_modified' not in record:
            return ("Data Integrity", False, "Missing modification timestamp")

        try:
            mod_time = datetime.datetime.fromisoformat(record['last_modified'])
            if (datetime.datetime.now() - mod_time) > datetime.timedelta(days=365):
                return ("Data Integrity", False, "Data not updated within last year")
        except (ValueError, TypeError):
            return ("Data Integrity", False, "Invalid timestamp format")

        return ("Data Integrity", True, "Data integrity checks passed")

    def _rule_access_security(self, record: Dict) -> Tuple[str, bool, str]:
        """Validate access security controls"""
        required_fields = ['access_id', 'auth_method', 'privilege_level']

        for field in required_fields:
            if field not in record:
                return ("Access Security", False, f"Missing security field: {field}")

        if record['auth_method'] not in ['mfa', 'saml', 'oauth']:
            return ("Access Security", False, f"Unsupported auth method: {record['auth_method']}")

        return ("Access Security", True, "Access security controls verified")

    def _rule_change_management(self, record: Dict) -> Tuple[str, bool, str]:
        """Ensure change management procedures are followed"""
        if 'change_id' not in record:
            return ("Change Management", False, "Missing change tracking identifier")

        if 'change_approver' not in record:
            return ("Change Management", False, "Missing change approver")

        return ("Change Management", True, "Change management controls in place")

    def _rule_monitoring(self, record: Dict) -> Tuple[str, bool, str]:
        """Verify system monitoring capabilities"""
        if 'monitoring_enabled' not in record or not record['monitoring_enabled']:
            return ("System Monitoring", False, "System monitoring not enabled")

        if 'alert_thresholds' not in record:
            return ("System Monitoring", False, "Missing alert configuration")

        return ("System Monitoring", True, "System monitoring properly configured")