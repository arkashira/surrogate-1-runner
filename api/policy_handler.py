import os
import uuid
import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, validator

router = APIRouter()

POLICY_DIR = "/opt/axentx/surrogate-1/policy/"

class Policy(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    rules: dict = Field(...)
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty or whitespace")
        return v.strip()

def ensure_policy_dir():
    """Ensure the policy directory exists."""
    if not os.path.exists(POLICY_DIR):
        os.makedirs(POLICY_DIR, exist_ok=True)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def upload_policy(policy: Policy):
    """Upload a new policy."""
    ensure_policy_dir()
    
    policy_id = str(uuid.uuid4())
    policy_file = os.path.join(POLICY_DIR, f"{policy_id}.json")
    
    try:
        with open(policy_file, "w") as f:
            json.dump(policy.dict(), f, indent=2)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to save policy: {str(e)}"
        )
    
    return {"policy_id": policy_id, "name": policy.name}

@router.get("/", response_model=List[dict])
async def list_policies():
    """List all policies."""
    ensure_policy_dir()
    
    policies = []
    for filename in os.listdir(POLICY_DIR):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(POLICY_DIR, filename), "r") as f:
                    policy_data = json.load(f)
                    policy_data["policy_id"] = filename.replace(".json", "")
                    policies.append(policy_data)
            except (json.JSONDecodeError, IOError):
                continue  # Skip corrupted files
    return policies

@router.get("/{policy_id}", response_model=dict)
async def get_policy(policy_id: str):
    """Get a specific policy by ID."""
    policy_file = os.path.join(POLICY_DIR, f"{policy_id}.json")
    
    if not os.path.exists(policy_file):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Policy {policy_id} not found"
        )
    
    try:
        with open(policy_file, "r") as f:
            policy_data = json.load(f)
            policy_data["policy_id"] = policy_id
            return policy_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read policy: {str(e)}"
        )