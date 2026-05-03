name: Ingest Surrogate-1 Training Pairs

on:
  workflow_dispatch:
    inputs:
      shard-id:
        description: 'Shard ID'
        required: true

jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Download pre-flight snapshot
        run: |
          ./bin/snapshot.sh ${{ inputs.shard-id }}

      - name: Ingest data
        run: |
          ./bin/dataset-enrich.sh ${{ inputs.shard-id }}