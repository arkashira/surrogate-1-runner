import pytest
from src.compliance_policy_enforcer import CompliancePolicyEnforcer
from src.compliance_policy_service import CompliancePolicyService
from src.database import get_db

@pytest.fixture
def db():
    return get_db()

def test_enforce_policies(db):
    policy_service = CompliancePolicyService(db)
    enforcer = CompliancePolicyEnforcer(policy_service)
    data = {"key": "value"}
    result = enforcer.enforce_policies(data)
    assert result is True