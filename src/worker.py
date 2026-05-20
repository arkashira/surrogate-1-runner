#!/usr/bin/env python3
"""
Worker that pulls a shard of the dataset from Hugging Face and processes it.
"""

import os
import requests
import json
import time

SHARD_ID = int(os.getenv("SHARD_ID", 0))
DATASET_URL = "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs"

def fetch_shard(shard_id: int) -> dict:
    """Download a single shard JSON file."""
    url = f"{DATASET_URL}/resolve/main/{shard_id}.json"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()

def process_data(data: dict):
    """Placeholder for whatever processing you need."""
    # Simulate some work
    time.sleep(2)
    # In a real job you would do something useful here
    print(f"Processed shard {data.get('shard_id', SHARD_ID)}")

def main():
    try:
        data = fetch_shard(SHARD_ID)
        process_data(data)
    except Exception as exc:
        print(f"[ERROR] Shard {SHARD_ID} failed: {exc}")
        # Let the container exit with a non‑zero status so Docker marks it unhealthy
        raise

if __name__ == "__main__":
    main()