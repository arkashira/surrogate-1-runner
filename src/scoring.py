"""Impact scoring logic for audit findings."""

from dataclasses import dataclass
from typing import Optional
from src.config import config


@dataclass
class ImpactScore:
    """Represents an calculated impact score."""
    policy_severity: int
    affected_resources: int
    business_value: int
    score: int


def calculate_impact_score(
    policy_severity: int,
    affected_resources: int,
    business_value: int
) -> ImpactScore:
    """
    Calculate impact score (0-100) based on three factors.
    
    Args:
        policy_severity: 0-10 (criticality of the policy violated)
        affected_resources: 0-10 (number/sensitivity of resources impacted)
        business_value: 0-10 (importance to business operations)
    
    Returns:
        ImpactScore with calculated score in range 0-100
    
    Formula: (severity * 5) + (resources * 3) + (business * 2)
    """
    # Clamp inputs to valid range
    severity = clamp(policy_severity)
    resources = clamp(affected_resources)
    business = clamp(business_value)
    
    # Calculate weighted score
    raw_score = (
        (severity * config.SEVERITY_WEIGHT) +
        (resources * config.RESOURCES_WEIGHT) +
        (business * config.BUSINESS_WEIGHT)
    )
    
    # Ensure within bounds (should always be 0-100 with current weights)
    score = max(0, min(100, raw_score))
    
    return ImpactScore(
        policy_severity=severity,
        affected_resources=resources,
        business_value=business,
        score=score
    )


def clamp(value: int, minimum: int = config.MIN_INPUT_VALUE, maximum: int = config.MAX_INPUT_VALUE) -> int:
    """Clamp a value to the specified range."""
    return max(minimum, min(maximum, value))