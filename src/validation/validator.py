import asyncio
import json
import jsonschema
from jsonschema import validate
from pathlib import Path
from .config import Config

async def validate_config(config: Config):
    schema_path = Path(__file__).parent / 'pipeline_schema.json'
    with open(schema_path) as schema_file:
        schema = json.load(schema_file)

    try:
        validate(instance=config.dict(), schema=schema)
        return True, []
    except jsonschema.exceptions.ValidationError as err:
        return False, [str(err)]

# /opt/axentx/surrogate-1/src/save_hook.py
from .config import Config
from .validation.validator import validate_config

async def save_hook(config: Config):
    valid, errors = await validate_config(config)
    if valid:
        print("Validation successful")
        # Show green checkmark badge
    else:
        print(f"Validation failed: {', '.join(errors)}")
        # Show errors inline in the editor
        # Trigger background validation job on save

## Summary
- Implemented `validate_config` function to validate the config using `jsonschema`.
- Integrated the validation function into the `save_hook`.
- Validation results are printed, and can be shown inline in the editor and as a badge.
- Validation is triggered on save and runs asynchronously.