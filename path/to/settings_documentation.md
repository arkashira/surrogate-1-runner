# Surrogate-1 Configuration Settings Documentation

## Overview
Surrogate-1 settings control data ingestion, normalization, and output behavior. Configure these in `bin/dataset-enrich.sh` or via environment variables.

## Core Settings Reference

| Setting Name         | Type   | Default        | Description                                                                 | Impact                                                                 |
|----------------------|--------|----------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------|
| `SHARD_ID`           | int    | 0              | Dataset partition identifier (0-15)                                       | Determines which 1/16th of the dataset is processed                    |
| `BATCH_SIZE`         | int    | 500            | Records processed per batch                                                 | Higher values = faster processing but more memory usage                |
| `NORMALIZATION_RULE` | string | "lowercase"    | Text normalization mode (lowercase, strip, none)                          | Affects text comparison accuracy and storage efficiency                |
| `DEDUP_THRESHOLD`    | float  | 0.95           | Similarity threshold for deduplication (0.0-1.0)                          | Lower values remove more near-duplicates                             |
| `OUTPUT_FORMAT`      | string | "jsonl"        | Output file format (jsonl, csv, parquet)                                  | Affects downstream tool compatibility                                  |
| `HASH_STORE_PATH`    | path   | "./hashes.db"  | SQLite database path for tracking duplicates                              | Change to persist across runs or use centralized storage               |

## Configuration Management

### Saving Settings