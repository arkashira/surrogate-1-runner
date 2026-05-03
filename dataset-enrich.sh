name: Ingest

on:
  workflow_dispatch:
    inputs:
      REPO:
        description: Dataset repository
        required: true
      PATH:
        description: Dataset path
        required: true

jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Download snapshot
        run: |
          curl -o snapshot.txt https://raw.githubusercontent.com/axentx/surrogate-1-runner/main/bin/snapshot.txt

      - name: Enrich dataset
        run: |
          ./bin/dataset-enrich.sh