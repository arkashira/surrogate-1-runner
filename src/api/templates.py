"""
API module for listing available data ingestion templates.

The templates are stored as JSON files under the repository root `templates/`.
Each JSON file must contain the keys:
  - name: str
  - description: str
  - parameters: dict

The endpoint `/templates` returns a list of all valid templates.
"""

from pathlib import Path
import json
from typing import Dict, List

from fastapi import APIRouter, HTTPException

router = APIRouter()

# Default templates directory relative to the repository root
TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"


def _load_template_file(file_path: Path) -> Dict:
    """
    Load a single template JSON file and validate required fields.
    """
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        raise ValueError(f"Failed to load template {file_path.name}: {exc}") from exc

    required_keys = {"name", "description", "parameters"}
    if not required_keys.issubset(data):
        missing = required_keys - data.keys()
        raise ValueError(f"Template {file_path.name} missing keys: {missing}")

    return data


@router.get("/templates", response_model=List[Dict])
def list_templates() -> List[Dict]:
    """
    Return a list of all available templates.

    Each template is represented as a dictionary with keys:
      - name
      - description
      - parameters
    """
    if not TEMPLATES_DIR.exists():
        raise HTTPException(status_code=404, detail="Templates directory not found")

    templates: List[Dict] = []
    for file_path in TEMPLATES_DIR.glob("*.json"):
        try:
            template = _load_template_file(file_path)
            templates.append(template)
        except ValueError:
            # Skip malformed templates silently
            continue

    return templates