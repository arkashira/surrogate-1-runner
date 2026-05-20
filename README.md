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

## Setup Process

To set up Surrogate-1, follow these steps:

1. Clone the repository: `git clone https://github.com/axentx/surrogate-1.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables: `cp .env.example .env` and edit `.env` to set your credentials
4. Run the setup script: `bin/setup.sh`
5. Verify the setup: `bin/verify-setup.sh`

## Guided Setup

The guided setup process is designed to be intuitive and easy to follow. It should take less than 15 minutes to complete on average, and users should be able to complete it without assistance.

## Troubleshooting

If you encounter any issues during the setup process, refer to the troubleshooting guide: [Troubleshooting](https://github.com/axentx/surrogate-1/blob/main/docs/TROUBLESHOOTING.md)