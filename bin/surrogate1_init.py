#!/usr/bin/env python3
import yaml
import json
import sys
from pathlib import Path

def validate_config(config):
    with open('/opt/axentx/surrogate-1/config_schema.json', 'r') as f:
        schema = json.load(f)

    # Basic validation - in a real scenario, use a proper validation library
    required_fields = ['version', 'dataset', 'workflow', 'logging']
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")

    dataset_fields = ['name', 'shard_id', 'shard_count']
    for field in dataset_fields:
        if field not in config['dataset']:
            raise ValueError(f"Missing required field in dataset: {field}")

    return True

def main():
    template_path = '/opt/axentx/surrogate-1/templates/default_surrogate.yaml'
    output_path = 'surrogate.yaml'

    try:
        with open(template_path, 'r') as f:
            config = yaml.safe_load(f)

        validate_config(config)

        with open(output_path, 'w') as f:
            yaml.dump(config, f)

        print(f"Successfully created {output_path}")
        print("\nTo launch the first worker, run:")
        print("surrogate1 run --shard-id 0\n")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()