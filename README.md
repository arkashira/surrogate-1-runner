# surrogate-1-runner

Parallel public-dataset ingest workers for the
[axentx/surrogate-1-training-pairs](https://huggingface.co/datasets/axentx/surrogate-1-training-pairs)
HuggingFace dataset.

## What this does

Every 30 minutes (or on `workflow_dispatch`), GitHub Actions launches **configurable parallel runners** (default 4). Each runner takes a deterministic slice of the public dataset list, streams, normalizes per-schema, dedups via the central md5 hash store, and uploads its output to a unique path on the dataset repo.

## Configuration

- Set the number of workers using the `WORKER_COUNT` environment variable.

## Summary

- Implemented configurable worker count using `WORKER_COUNT` environment variable.
- Updated README to reflect the change.