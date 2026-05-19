import os
import json
import yaml
import git
from typing import Dict, Any

class PolicyLoader:
    def __init__(self, policy_dir: str):
        self.policy_dir = policy_dir
        self.repo = git.Repo(self.policy_dir)

    def load_policy(self, policy_id: str) -> Dict[str, Any]:
        policy_path = os.path.join(self.policy_dir, f"{policy_id}.yaml")
        if not os.path.exists(policy_path):
            raise FileNotFoundError(f"Policy {policy_id} not found")

        with open(policy_path, "r") as f:
            policy = yaml.safe_load(f)

        return policy

    def get_current_policy(self, policy_id: str) -> Dict[str, Any]:
        policy = self.load_policy(policy_id)
        version = self.repo.head.commit.hexsha
        return {"policy": policy, "version": version}

# /opt/axentx/surrogate-1/api/policy.py
from fastapi import APIRouter, HTTPException
from policy.loader import PolicyLoader

router = APIRouter(prefix="/policy", tags=["Policy"])

@router.get("/{policy_id}")
def get_policy(policy_id: str, policy_loader: PolicyLoader = Depends(PolicyLoader)):
    try:
        return policy_loader.get_current_policy(policy_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Policy not found")

# /opt/axentx/surrogate-1/main.py
from fastapi import FastAPI
from api.policy import router as policy_router

app = FastAPI()

app.include_router(policy_router)

## Summary
- Implemented `PolicyLoader` class to load policies from a Git-backed directory.
- Created API endpoint `/policy/{id}` to return the current policy.
- Integrated policy loader with the main application.