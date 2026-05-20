
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any
from datetime import datetime
from surrogate_1.database import get_db
from surrogate_1.models import DecisionAudit

audit_db = get_db

async def audit_middleware(func):
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        decision_id = kwargs.get('decision_id')
        policy_id = kwargs.get('policy_id')
        context_hash = kwargs.get('context_hash')
        decision_output = str(result)

        if decision_id and policy_id and context_hash and decision_output:
            db = audit_db()
            new_audit = DecisionAudit(
                decision_id=decision_id,
                policy_id=policy_id,
                policy_version=1,  # Assuming version 1 for the first log
                context_hash=context_hash,
                timestamp=datetime.utcnow(),
                decision_output=decision_output
            )
            db.add(new_audit)
            db.commit()

        return result

    return wrapper