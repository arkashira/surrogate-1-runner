import pytest
from src.compliance_policy_service import CompliancePolicyService
from src.database import get_db

@pytest.fixture
def db():
    return get_db()

def test_create_policy(db):
    policy_service = CompliancePolicyService(db)
    policy_data = {
        "id": "1",
        "name": "Test Policy",
        "description": "This is a test policy",
        "is_active": True,
        "rules": ["rule1", "rule2"]
    }
    policy = policy_service.create_policy(policy_data)
    assert policy.id == "1"
    assert policy.name == "Test Policy"
    assert policy.description == "This is a test policy"
    assert policy.is_active
    assert policy.rules == ["rule1", "rule2"]