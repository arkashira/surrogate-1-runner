/opt/axentx/surrogate-1/
│
├─ services/
│   ├─ __init__.py
│   ├─ metrics.py          # core logic + optional persistence
│   └─ api.py              # Flask app exposing the HTTP endpoints
│
└─ tests/
    └─ test_metrics.py