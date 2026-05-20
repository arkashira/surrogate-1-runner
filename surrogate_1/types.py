from dataclasses import dataclass

@dataclass
class Detection:
    rule_id: str       # Unique rule identifier
    severity: str      # LOW, MEDIUM, HIGH, or CRITICAL
    message: str       # Human-readable description
    location: str      # File path or URL