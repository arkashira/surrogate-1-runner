src/
├─ email/
│   ├─ mod.rs          ← trait, concrete SMTP impl, mock impl, templates, errors
│   └─ smtp.rs         ← thin wrapper around lettre
├─ credit_alert/
│   └─ mod.rs          ← monitor, config structs, rate‑limiting logic
└─ lib.rs              ← re‑exports for easy consumption