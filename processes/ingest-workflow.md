# Surrogate-1 Ingest Workflow Process

## Overview

This document describes the core ingest workflow that runs every 30 minutes to process public datasets into the [axentx/surrogate-1-training-pairs](https://huggingface.co/datasets/axentx/surrogate-1-training-pairs) HuggingFace dataset.

## Trigger Conditions

1. **Scheduled**: Cron job runs every 30 minutes
2. **Manual**: GitHub Actions `workflow_dispatch` event

## Workflow Execution

### Step 1: Launch Parallel Runners

GitHub Actions launches **16 parallel runners** (defined in `.github/workflows/ingest.yml`).

### Step 2: Shard Assignment

Each runner receives a deterministic 1/16 slice of the dataset list:
- **Shard ID**: Computed from `slug-hash bucket`
- **Deterministic**: Same dataset always goes to same runner (for deduplication consistency)

### Step 3: Data Processing

Each runner:
1. Streams its assigned portion of the public dataset list
2. Normalizes data per-schema (see `bin/dataset-enrich.sh`)
3. Deduplicates via the central md5 hash store
4. Uploads output to a unique path on the HuggingFace dataset repo

### Step 4: Completion

All 16 runners must complete before the next scheduled run.

## Running the Workflow

### Automated (Production)
The workflow runs automatically every 30 minutes via the scheduled cron job.

### Manual Trigger