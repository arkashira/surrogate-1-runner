from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class TemplateMetadata(BaseModel):
    id: str = Field(..., description="Unique identifier for the template")
    name: str = Field(..., description="Name of the template")
    description: str = Field(..., description="Description of the template")
    category: str = Field(..., description="Category of the template")
    tags: List[str] = Field(..., description="Tags associated with the template")
    version: str = Field(..., description="Version of the template")
    author: str = Field(..., description="Author of the template")
    created_at: str = Field(..., description="Creation date of the template")
    updated_at: str = Field(..., description="Last update date of the template")

class TemplateSchema(BaseModel):
    metadata: TemplateMetadata = Field(..., description="Metadata of the template")
    parameters: Dict[str, Dict] = Field(..., description="Parameters of the template")
    workflow: Dict = Field(..., description="Workflow definition of the template")