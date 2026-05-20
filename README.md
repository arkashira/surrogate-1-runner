surrogate-1/
├── bin/
│   ├── dataset-enrich.sh    # Dataset list and enrichment logic
│   ├── ingest.sh            # Per-shard ingestion script
│   └── normalize.sh         # Schema normalization
├── src/
│   ├── dedup.go             # MD5 deduplication client
│   ├── stream.go            # Dataset streaming
│   └── upload.go            # HuggingFace upload
├── examples/
│   └── sample_app.py        # Sample integration app
├── config.json              # Optional configuration file
├── requirements.txt         # Python dependencies
├── .github/
│   └── workflows/
│       └── ingest.yml       # GitHub Actions workflow
└── README.md