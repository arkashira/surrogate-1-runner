from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from src.validators.config_validator import validate_config

router = APIRouter()

@router.post('/config')
async def update_config(config_data: Dict[str, Any]):
    try:
        validated_config = validate_config(config_data)
        # Save the validated configuration to the database or file system
        # For now, we'll just return the validated configuration
        return {'message': 'Configuration updated successfully', 'config': validated_config}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))