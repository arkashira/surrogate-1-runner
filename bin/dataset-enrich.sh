name: Ingest Public Dataset

on:
  workflow_dispatch:
    inputs:
      DATE:
        description: 'Date to ingest (YYYY-MM-DD)'
        required: true
      REPO:
        description: 'Repository to ingest'
        required: true

jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Run pre-flight snapshot generation
        run: |
          bin/snapshot.sh ${{ inputs.DATE }} ${{ inputs.REPO }}

      - name: Run dataset enrichment
        run: |
          bin/dataset-enrich.sh ${{ inputs.DATE }} ${{ inputs.REPO }}