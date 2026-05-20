my‑ingest‑project/
├─ src/
│  ├─ __init__.py
│  └─ ingest/
│     ├─ __init__.py
│     ├─ cli.py          # tiny argparse wrapper
│     ├─ core.py         # pure ingestion logic (see below)
│     └─ config.py       # config loading & validation
├─ tests/
│  └─ test_ingest.py
├─ config.yaml           # optional user config
├─ datasets.txt          # one ID per line
├─ pyproject.toml
└─ README.md