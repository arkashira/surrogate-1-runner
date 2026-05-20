#!/usr/bin/env python3
"""CLI for surrogate-1 dataset management."""

import argparse
import sys
import yaml
import requests
from pathlib import Path


def load_config(config_path: str = "/opt/axentx/surrogate-1/config.yaml") -> dict:
    """Load configuration from YAML file."""
    path = Path(config_path)
    if not path.exists():
        return {"sources": []}
    with open(path, "r") as f:
        return yaml.safe_load(f) or {"sources": []}


def save_config(config: dict, config_path: str = "/opt/axentx/surrogate-1/config.yaml") -> None:
    """Save configuration to YAML file."""
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)


def validate_url(url: str) -> bool:
    """Validate that a URL is reachable."""
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        return response.status_code < 400
    except requests.RequestException:
        return False


def add_source(url: str, config_path: str = "/opt/axentx/surrogate-1/config.yaml") -> int:
    """Add a new dataset source to the configuration."""
    # Validate URL is reachable
    print(f"Validating URL: {url}")
    if not validate_url(url):
        print(f"Error: URL {url} is not reachable", file=sys.stderr)
        return 1
    
    # Load existing config
    config = load_config(config_path)
    
    # Initialize sources list if not present
    if "sources" not in config:
        config["sources"] = []
    
    # Check for duplicate
    if url in config["sources"]:
        print(f"Source {url} already exists in config")
        return 0
    
    # Add the new source
    config["sources"].append(url)
    
    # Save config
    save_config(config, config_path)
    print(f"Added source: {url}")
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="surrogate-1",
        description="CLI for surrogate-1 dataset management"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # add-source command
    add_parser = subparsers.add_parser(
        "add-source",
        help="Add a new dataset source"
    )
    add_parser.add_argument(
        "url",
        help="URL of the dataset source to add"
    )
    add_parser.add_argument(
        "--config",
        default="/opt/axentx/surrogate-1/config.yaml",
        help="Path to config file (default: /opt/axentx/surrogate-1/config.yaml)"
    )
    
    args = parser.parse_args()
    
    if args.command == "add-source":
        return add_source(args.url, args.config)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())