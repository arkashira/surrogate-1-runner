name: Ingest Public Dataset

on:
  workflow_dispatch:
    inputs:
      date_folder:
        description: 'Date folder to ingest'
        required: true

jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Run pre-flight snapshot generation
        run: |
          ./bin/snapshot.sh

      - name: Run training script
        run: |
          ./train.py