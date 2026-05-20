import argparse
import json
import os
import sys
from pathlib import Path

import yaml
from jsonschema import Draft7Validator, ValidationError

# Path to the schema file relative to this module
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "config_schema.json"

# Default configuration values
DEFAULT_CONFIG = {
    "dataset_path": "datasets/public",
    "worker_count": 16,
    "api_key": "YOUR_API_KEY_HERE",
    "shard_id": 0,
    "output_dir": "output",
    "log_level": "INFO",
}


def load_schema():
    """Load JSON schema from file."""
    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading schema: {e}", file=sys.stderr)
        sys.exit(1)


def validate_config(config, schema):
    """Validate config dict against the provided JSON schema."""
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(config), key=lambda e: e.path)
    if errors:
        for err in errors:
            path = ".".join(map(str, err.path)) or "<root>"
            print(f"Configuration error at '{path}': {err.message}", file=sys.stderr)
        sys.exit(1)


def init_config(args):
    """Create a surrogate.yaml file with default values and validate it."""
    config_path = Path(args.output or "surrogate.yaml")
    if config_path.exists():
        print(f"Configuration file '{config_path}' already exists. Aborting.", file=sys.stderr)
        sys.exit(1)

    # Write defaults to YAML
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(DEFAULT_CONFIG, f, sort_keys=False)
    except Exception as e:
        print(f"Failed to write configuration file: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate the written config
    schema = load_schema()
    validate_config(DEFAULT_CONFIG, schema)

    print(f"✅ Configuration file created at '{config_path}'.")
    print("To launch the first worker, run:")
    print(f"   surrogate1 worker --config {config_path} --shard 0")
    sys.exit(0)


def worker(args):
    """Placeholder for the worker command."""
    # The actual worker implementation is omitted for brevity.
    print("Worker command invoked with args:", args)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="surrogate1",
        description="Surrogate-1 CLI for dataset ingestion and worker orchestration.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init subcommand
    init_parser = subparsers.add_parser(
        "init",
        help="Create a new surrogate.yaml configuration file with default values.",
    )
    init_parser.add_argument(
        "-o",
        "--output",
        help="Path to write the configuration file (default: surrogate.yaml in current dir).",
    )
    init_parser.set_defaults(func=init_config)

    # worker subcommand (simplified)
    worker_parser = subparsers.add_parser(
        "worker",
        help="Run a surrogate ingestion worker.",
    )
    worker_parser.add_argument(
        "--config",
        required=True,
        help="Path to surrogate.yaml configuration file.",
    )
    worker_parser.add_argument(
        "--shard",
        type=int,
        required=True,
        help="Shard ID to process (0-15).",
    )
    worker_parser.set_defaults(func=worker)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()