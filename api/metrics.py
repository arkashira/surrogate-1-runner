/opt/axentx/surrogate-1/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI entry point
│   └── metrics.py            # <-- core implementation (see below)
├── logs/
│   └── enable_events.log    # auto‑created if missing
├── tests/
│   └── test_metrics.py
├── Dockerfile
└── requirements.txt