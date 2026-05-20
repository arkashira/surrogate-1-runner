# surrogate-1-runner

Parallel public-dataset ingest workers for the [axentx/surrogate-1](https://github.com/axentx/surrogate-1) project.

## What this does

Every 30 minutes (or on `workflow_dispatch`), GitHub Actions launches **16 parallel runners**. Each runner takes a deterministic 1/16 slice (`slug-hash bucket = SHARD_ID`) of the public dataset list defined in `bin/dataset-enrich.sh`, streams, normalizes per-schema, dedups via the central md5 hash store, and uploads its output to a unique path on the dataset repo:

## Quick Start Guide

1. **Clone the repository**: