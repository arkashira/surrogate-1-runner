# surrogate-1-runner

## Overview

The `surrogate-1-runner` is designed to manage parallel public-dataset ingest workers for the
[axentx/surrogate-1-training-pairs](https://huggingface.co/datasets/axentx/surrogate-1-training-pairs)
HuggingFace dataset.

## Functionality

Every 30 minutes (or on `workflow_dispatch`), GitHub Actions launches **16 parallel runners**.
Each runner processes a deterministic 1/16 slice of the public dataset list defined in `bin/dataset-enrich.sh`. The process includes streaming, normalizing per-schema, deduplication via a central MD5 hash store, and uploading the output to a unique path in the dataset repository.

## CLI Command

To manually trigger the agent, use the following command: