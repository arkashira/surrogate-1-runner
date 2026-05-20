from typing import List, Dict, Any
from pydantic import BaseModel, Field, validator

class Rule(BaseModel):
    id: str
    action: str = Field(..., regex="^(allow|deny|audit)$")
    condition: Dict[str, Any]
    description: str | None = None

class Policy(BaseModel):
    name: str
    version: str
    description: str | None = None
    rules: List[Rule]

    @validator("version")
    def semver(cls, v):
        # Very light check – replace with a proper semver lib if needed
        if not v.count(".") == 2:
            raise ValueError("version must be semver (e.g. 1.0.0)")
        return v