import pytest
from datetime import datetime
from src.compliance_policy import CompliancePolicy

def test_compliance_policy_creation():
    policy_data = {
        "id": "1",
        "name": "Test Policy",
        "description": "This is a test policy",
        "is_active": True,
        "rules": ["rule1", "rule2"]
    }
    policy = CompliancePolicy(**policy_data)
    assert policy.id == "1"
    assert policy.name == "Test Policy"
    assert policy.description == "This is a test policy"
    assert policy.is_active
    assert policy.rules == ["rule1", "rule2"]
    assert isinstance(policy.created_at, datetime)
    assert isinstance(policy.updated_at, datetime)