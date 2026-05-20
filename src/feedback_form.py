/opt/axentx/surrogate-1/
│
├─ src/
│   ├─ __init__.py
│   ├─ feedback_form.py      # CLI + optional GUI
│   ├─ feedback_handler.py   # Background uploader / analyzer
│   └─ ide_integration.py    # Tiny wrapper used by the IDE plug‑in
│
└─ data/
    └─ feedback.json         # Persistent local store (created at runtime)