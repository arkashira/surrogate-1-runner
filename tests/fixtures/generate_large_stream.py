#!/usr/bin/env python3
"""
Generate a 1GB synthetic NDJSON fixture for memory-bound testing.
Deterministic output for reproducible CI runs.
"""

import hashlib
import json
import os
import sys
from typing import Iterator, Dict, Any

# Configuration
OUTPUT_PATH = os.environ.get("FIXTURE_PATH", "/opt/axentx/surrogate-1/tests/fixtures/large_stream.ndjson")
TARGET_SIZE_MB = 1024  # 1GB
RECORD_SIZE_TARGET_BYTES = 2048  # ~2KB per record for ~500k records


def generate_record(seed: int) -> Dict[str, Any]:
    """Generate a deterministic NDJSON record."""
    return {
        "id": seed,
        "hash": hashlib.md5(str(seed).encode()).hexdigest(),
        "timestamp": f"2026-05-21T{(seed % 86400):02d}:{(seed % 60):02d}:00Z",
        "payload": {
            "data": "x" * (seed % 500),
            "metadata": {
                "version": f"1.{seed % 10}.{seed % 100}",
                "source": f"shard_{seed % 16}",
                "checksum": hashlib.sha256(str(seed).encode()).hexdigest()[:16]
            }
        },
        "flags": [f"flag_{i}" for i in range((seed % 10) + 1)]
    }


def generate_stream(seed: int = 42) -> Iterator[str]:
    """Generate NDJSON records deterministically."""
    current = seed
    while True:
        record = generate_record(current)
        yield json.dumps(record, separators=(',', ':'))
        current += 1


def main():
    """Generate the fixture file."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        record_count = 0
        current_size = 0
        
        for line in generate_stream():
            f.write(line + '\n')
            current_size += len(line) + 1  # +1 for newline
            record_count += 1
            
            # Progress indicator every 100k records
            if record_count % 100000 == 0:
                print(f"Generated {record_count} records, ~{current_size / 1024 / 1024:.2f}MB", file=sys.stderr)
    
    # Write checksum file
    checksum_path = os.path.join(os.path.dirname(OUTPUT_PATH), "large_stream.sha256")
    with open(checksum_path, 'w', encoding='utf-8') as f:
        with open(OUTPUT_PATH, 'rb') as data:
            checksum = hashlib.sha256(data.read()).hexdigest()
        f.write(f"{checksum}  large_stream.ndjson\n")
    
    print(f"Fixture generated: {OUTPUT_PATH}")
    print(f"Records: {record_count}")
    print(f"Size: {current_size / 1024 / 1024:.2f}MB")
    print(f"Checksum: {checksum}", file=sys.stderr)


if __name__ == "__main__":
    main()