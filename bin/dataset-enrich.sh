name: Ingest

on:
  workflow_dispatch:
    inputs:
      shard_id:
        description: Shard ID
        required: true

jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Run dataset-enrich.sh
        run: |
          bin/dataset-enrich.sh ${{ inputs.shard_id }}
        retry: 3
        retry-on: failure