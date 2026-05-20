"""
Anonymizer module for synthetic sandbox data.

ASSUMPTIONS MADE (must be validated against regulatory requirements):
- "Anonymization" here means PII masking for development/test environments
- This may NOT satisfy GDPR Article 89 or HIPAA Safe Harbor requirements
- True anonymization may require k-anonymity, differential privacy, or data synthesis

SECURITY NOTE: The salt is read from environment for production use.
"""

import re
import os
import hashlib
from typing import Any, Dict, Optional

# Regular expressions for detecting common PII patterns
EMAIL_RE = re.compile(r"(?P<local>[^@]+)@(?P<domain>[^@]+\.[^@]+)")
PHONE_RE = re.compile(r"\b(?:\+?(\d{1,3})[-.\s]?)?(?:\(?(\d{3})\)?[-.\s]?)?(\d{3})[-.\s]?(\d{4})\b")
NAME_RE = re.compile(r"\b[A-Z][a-z]+(?:[-'][A-Z][a-z]+)*\b")
# Extended patterns for additional PII
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

# Salt from environment (fallback for development only)
_SALT = os.environ.get("ANONYMIZER_SALT", "dev-only-salt-do-not-use-in-prod")

def _hash_value(value: str, prefix: str = "") -> str:
    """Hash a value with salt, return prefixed result."""
    hasher = hashlib.sha256()
    hasher.update((_SALT + value).encode("utf-8"))
    return f"{prefix}{hasher.hexdigest()[:12]}"

def anonymize_email(email: str) -> str:
    """Replace local part with deterministic hash, preserve domain."""
    match = EMAIL_RE.match(email)
    if not match:
        return email
    local_hash = _hash_value(match.group('local'), "anon_")
    return f"{local_hash}@{match.group('domain')}"

def anonymize_phone(phone: str) -> str:
    """Redact all digits in phone numbers."""
    def repl(match):
        return "X" * len(match.group(0))
    return PHONE_RE.sub(repl, phone)

def anonymize_name(name: str) -> str:
    """Replace name with deterministic hash (not true anonymization)."""
    return _hash_value(name, "person_")

def anonymize_ssn(ssn: str) -> str:
    """Redact SSN completely."""
    return "XXX-XX-XXXX"

def anonymize_ip(ip: str) -> str:
    """Generalize IP to /24 network."""
    match = IP_RE.match(ip)
    if match:
        parts = ip.split('.')
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
    return ip

def anonymize_record(record: Dict[str, Any], fields_to_anonymize: Optional[list] = None) -> Dict[str, Any]:
    """
    Anonymize a single data record.
    
    Parameters
    ----------
    record : dict
        Data record with field names as keys.
    fields_to_anonymize : list, optional
        Explicit list of fields to anonymize. If None, auto-detect.
    
    Returns
    -------
    dict
        Record with PII fields anonymized.
    """
    anonymized = {}
    
    for key, value in record.items():
        # Skip if field explicitly excluded
        if fields_to_anonymize and key not in fields_to_anonymize:
            anonymized[key] = value
            continue
            
        if not isinstance(value, str):
            anonymized[key] = value
            continue
        
        # Auto-detection pipeline (first match wins)
        if SSN_RE.search(value):
            anonymized[key] = anonymize_ssn(value)
        elif EMAIL_RE.search(value):
            anonymized[key] = anonymize_email(value)
        elif PHONE_RE.search(value):
            anonymized[key] = anonymize_phone(value)
        elif NAME_RE.search(value):
            anonymized[key] = anonymize_name(value)
        elif IP_RE.search(value):
            anonymized[key] = anonymize_ip(value)
        else:
            anonymized[key] = value
    
    return anonymized