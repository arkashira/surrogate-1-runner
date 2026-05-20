# surrogate-1-runner

Parallel public-dataset ingest workers for the
[axentx/surrogate-1-training-pairs](https://huggingface.co/datasets/axentx/surrogate-1-training-pairs)
HuggingFace dataset.

## What this does

Every 30 minutes (or on `workflow_dispatch`), GitHub Actions launches **16 parallel runners**.
Each runner takes a deterministic 1/16 slice (`slug-hash bucket = SHARD_ID`)
of the public dataset list defined in `bin/dataset-enrich.sh`, streams,
normalizes per-schema, dedups via the central md5 hash store, and uploads
its output to a unique path on the dataset repo:

## CLI Usage

The surrogate-1 CLI provides commands to manage dataset sources:

### Add a new dataset source