name: Ingest

on:
  workflow_dispatch:
    inputs:
      DATE:
        description: 'Date folder to process'
        required: true

jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Generate pre-flight snapshot
        run: |
          ./bin/snapshot.sh

      - name: Process file list from snapshot
        run: |
          ./bin/dataset-enrich.sh
        error: on-failure
        continue-on-error: true