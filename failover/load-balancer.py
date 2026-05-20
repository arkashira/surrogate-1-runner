/opt/axentx/surrogate-1/
│
├─ load_balancer/
│   ├─ __init__.py
│   ├─ core.py          # <-- the implementation below
│   └─ config.py        # optional helper for env‑based config
│
└─ tests/
    └─ failover/
        └─ test_load_balancer.py