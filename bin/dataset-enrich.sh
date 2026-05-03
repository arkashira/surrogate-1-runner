name: Ingest

on:
  workflow_dispatch:
    inputs:
      date:
        description: 'Date folder to process'
        required: true

jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Run snapshot script
        run: |
          bin/snapshot.sh
      - name: Run dataset-enrich script
        run: |
          bin/dataset-enrich.sh