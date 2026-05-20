from typing import List, Optional
from fastapi import HTTPException
from .compliance_policy import CompliancePolicy
from .database import get_db

class CompliancePolicyService:
    def __init__(self, db):
        self.db = db

    async def create_policy(self, policy_data: dict) -> CompliancePolicy:
        policy = CompliancePolicy(**policy_data)
        self.db.add(policy)
        self.db.commit()
        self.db.refresh(policy)
        return policy

    async def get_policy(self, policy_id: str) -> Optional[CompliancePolicy]:
        return self.db.query(CompliancePolicy).filter(CompliancePolicy.id == policy_id).first()

    async def update_policy(self, policy_id: str, policy_data: dict) -> CompliancePolicy:
        policy = await self.get_policy(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        for key, value in policy_data.items():
            setattr(policy, key, value)
        policy.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(policy)
        return policy

    async def list_policies(self) -> List[CompliancePolicy]:
        return self.db.query(CompliancePolicy).all()