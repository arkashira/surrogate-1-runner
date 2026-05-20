from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class IntegrationConfig(BaseModel):
    organization_id: str
    api_key: str
    custom_settings: Optional[dict] = None

@app.post("/integrate")
async def integrate(config: IntegrationConfig):
    # Validate the integration configuration
    if not config.organization_id or not config.api_key:
        raise HTTPException(status_code=400, detail="Organization ID and API key are required")

    # Securely store the integration configuration
    # This is a placeholder for actual secure storage logic
    store_integration_config(config)

    # Return a success message
    return {"message": "Integration successful", "organization_id": config.organization_id}

def store_integration_config(config: IntegrationConfig):
    # Placeholder for secure storage logic
    # In a real implementation, this would securely store the integration configuration
    pass

@app.get("/integration/{organization_id}")
async def get_integration(organization_id: str):
    # Retrieve the integration configuration
    # This is a placeholder for actual retrieval logic
    config = retrieve_integration_config(organization_id)

    if not config:
        raise HTTPException(status_code=404, detail="Integration not found")

    return config

def retrieve_integration_config(organization_id: str):
    # Placeholder for retrieval logic
    # In a real implementation, this would retrieve the integration configuration
    pass