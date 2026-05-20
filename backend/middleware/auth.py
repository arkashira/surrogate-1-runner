/opt/axentx/surrogate-1/backend/
│
├─ middleware/
│   └─ auth.py          # Auth + rate‑limit middleware
│
├─ routers/
│   └─ credits.py       # /api/v1/credits/{account_id}
│
├─ services/
│   └─ credit_service.py
│
├─ schemas/
│   └─ credits.py
│
├─ main.py              # FastAPI app bootstrap
└─ openapi.yaml          # (optional static copy)