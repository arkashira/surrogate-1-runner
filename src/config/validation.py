import json
import jsonschema
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import yaml
from pathlib import Path

def load_schema():
    """Load the JSON schema for configuration validation."""
    schema_path = Path(__file__).parent.parent / 'config_schema.json'
    with open(schema_path, 'r') as f:
        return json.load(f)

def validate_config(config_path):
    """Validate the configuration file against the schema."""
    schema = load_schema()
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    try:
        validate(instance=config, schema=schema)
        return True, None
    except ValidationError as e:
        return False, str(e)

def validate_required_fields(config):
    """Validate that required fields are present in the configuration."""
    required_fields = ['dataset_name', 'shard_id', 'output_path']
    missing_fields = [field for field in required_fields if field not in config]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    return True, None