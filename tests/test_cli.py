#!/usr/bin/env python3
"""CLI for surrogate-1 dataset management.
Usage:
    surrogate-1 add-source <url>    Add a new dataset source
    surrogate-1 list-sources         List all configured sources
    surrogate-1 remove-source <url> Remove a dataset source
"""

import argparse
import sys
import os
import yaml
from pathlib import Path
from datetime import datetime
import requests
from typing import Dict, List, Optional, Union

# Configuration path
CONFIG_PATH = Path(__file__).parent / "config.yaml"

def load_config() -> Dict:
    """Load configuration from config.yaml."""
    if not CONFIG_PATH.exists():
        return {'sources': [], 'settings': {}}
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

def save_config(config: Dict) -> None:
    """Save configuration to config.yaml."""
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

def validate_url(url: str, timeout: int = 10) -> bool:
    """Validate that a URL is reachable.

    Args:
        url: The URL to validate
        timeout: Connection timeout in seconds

    Returns:
        True if the URL is reachable

    Raises:
        ValueError: If URL schema is invalid
        Exception: If URL is not reachable
    """
    # Check for valid schema
    if not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL schema. Must start with http:// or https://")

    # Try to reach the URL
    try:
        response = requests.head(
            url,
            timeout=timeout,
            allow_redirects=True
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        raise Exception(f"URL {url} is not reachable: {str(e)}")

def add_source(url: str) -> bool:
    """Add a new dataset source to the configuration.

    Args:
        url: The URL of the dataset source to add

    Returns:
        True if the source was added, False if it already exists
    """
    config = load_config()

    # Check if source already exists
    if any(source['url'] == url for source in config['sources']):
        return False

    # Validate URL before adding
    validate_url(url)

    # Add new source
    config['sources'].append({
        'url': url,
        'added_at': datetime.now().isoformat(),
        'status': 'active'
    })

    save_config(config)
    return True

def list_sources() -> List[Dict]:
    """List all configured sources."""
    config = load_config()
    return config.get('sources', [])

def remove_source(url: str) -> bool:
    """Remove a dataset source from configuration.

    Args:
        url: The URL of the source to remove

    Returns:
        True if source was removed, False if not found
    """
    config = load_config()
    initial_count = len(config['sources'])

    config['sources'] = [
        source for source in config['sources']
        if source['url'] != url
    ]

    if len(config['sources']) == initial_count:
        return False

    save_config(config)
    return True

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='surrogate-1 dataset management')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Add source command
    add_parser = subparsers.add_parser('add-source', help='Add a new dataset source')
    add_parser.add_argument('url', help='URL of the dataset source')

    # List sources command
    subparsers.add_parser('list-sources', help='List all configured sources')

    # Remove source command
    remove_parser = subparsers.add_parser('remove-source', help='Remove a dataset source')
    remove_parser.add_argument('url', help='URL of the source to remove')

    args = parser.parse_args()

    try:
        if args.command == 'add-source':
            if add_source(args.url):
                print(f"Successfully added source: {args.url}")
            else:
                print(f"Source already exists: {args.url}")

        elif args.command == 'list-sources':
            sources = list_sources()
            if not sources:
                print("No sources configured")
            else:
                print("Configured sources:")
                for source in sources:
                    print(f"- {source['url']} (added: {source['added_at']})")

        elif args.command == 'remove-source':
            if remove_source(args.url):
                print(f"Successfully removed source: {args.url}")
            else:
                print(f"Source not found: {args.url}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()