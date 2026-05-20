/opt/axentx/surrogate-1/
│
├─ src/
│   ├─ api/
│   │   └─ slack_endpoint.py   ← **this file**
│   ├─ core/
│   │   └─ vault.py            ← thin wrapper around your secrets‑vault (example provided)
│   └─ __init__.py
│
├─ tests/
│   └─ test_slack_endpoint.py  ← pytest suite (example snippets at the bottom)
│
└─ requirements.txt