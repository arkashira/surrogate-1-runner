name: Ingest

on:
  workflow_dispatch:
    inputs:
      slug:
        description: 'Slug hash to ingest'
        required: true

jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Docker
        uses: docker/setup-docker@v1

      - name: Run ingest script
        run: |
          bin/dataset-enrich.sh