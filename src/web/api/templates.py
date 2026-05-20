from fastapi import APIRouter
from typing import List
import yaml
import os

router = APIRouter()

TEMPLATES_DIR = "/opt/axentx/surrogate-1/templates/library"

@router.get("/templates", response_model=List[dict])
async def get_templates():
    """
    Endpoint to retrieve available templates from the templates library.

    Returns:
        List[dict]: A list of template dictionaries containing 'name' and 'description'.
    """
    templates = []
    for filename in os.listdir(TEMPLATES_DIR):
        if filename.endswith(".yaml"):
            with open(os.path.join(TEMPLATES_DIR, filename), "r") as file:
                template = yaml.safe_load(file)
                templates.append({
                    "name": filename[:-5],  # Remove .yaml extension
                    "description": template.get("description", "")
                })
    return templates