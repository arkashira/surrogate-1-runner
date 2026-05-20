import sys
import yaml
import json
from jsonschema import validate, ValidationError
from pathlib import Path

# Define the schema for Config.yaml
CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "dataset_repo": {"type": "string", "format": "uri"},
        "shard_count": {"type": "integer", "minimum": 1, "maximum": 32},
        "batch_size": {"type": "integer", "minimum": 1},
        "upload": {
            "type": "object",
            "properties": {
                "target_repo": {"type": "string"},
                "path_prefix": {"type": "string"},
                "auth_method": {"type": "string", "enum": ["token", "ssh", "oauth"]}
            },
            "required": ["target_repo", "path_prefix", "auth_method"]
        },
        "enrichment": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "enabled": {"type": "boolean"},
                    "timeout_seconds": {"type": "integer", "minimum": 1}
                },
                "required": ["name", "enabled"]
            }
        }
    },
    "required": ["dataset_repo", "shard_count", "batch_size", "upload", "enrichment"],
    "additionalProperties": False
}

def load_yaml_file(filepath: Path):
    """Load and parse YAML file, with error handling."""
    try:
        return yaml.safe_load(filepath.read_text())
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error in {filepath}: {e}")
        return None
    except Exception as e:
        print(f"❌ Error reading file {filepath}: {e}")
        return None

def validate_config(filepath: Path) -> bool:
    """Validate a Config.yaml file against the schema."""
    config_data = load_yaml_file(filepath)
    if config_data is None:
        return False

    try:
        validate(instance=config_data, schema=CONFIG_SCHEMA)
        print(f"✅ {filepath} is valid.")
        return True
    except ValidationError as e:
        # Provide clear, actionable error message
        err_path = ".".join(str(p) for p in e.absolute_path) if e.absolute_path else "root"
        print(f"❌ Validation failed: {e.message}")
        print(f"   Path: {err_path}")
        print(f"   Value: {e.instance}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during validation: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: config-validator.py <path-to-config.yaml>")
        sys.exit(1)

    config_path = Path(sys.argv[1])
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        sys.exit(1)

    success = validate_config(config_path)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()