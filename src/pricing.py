/opt/axentx/surrogate-1/
│
├─ src/
│   ├─ __init__.py
│   ├─ pricing.py          # PricingService + provider helpers
│   ├─ routing.py          # RoutingService (cheapest provider + health)
│   └─ generate_text.py    # Public helper that uses RoutingService
│
├─ tests/
│   ├─ __init__.py
│   ├─ test_pricing.py
│   └─ test_routing.py
│
├─ requirements.txt
└─ README.md