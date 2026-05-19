
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

policies: Dict[str, str] = {}

@app.get("/policy/{policy_id}")
async def read_policy(policy_id: str):
    if policy_id not in policies:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policies[policy_id]

@app.post("/policy")
async def create_policy(policy: Policy):
    policies[policy.id] = policy.dict()
    return {"message": "Policy created"}

class Policy(BaseModel):
    id: str
    content: str