
### Why this layout?

* **Single entry point** – `make dev-setup` does everything a new contributor expects.  
* **Opt‑out flag** – `NO_HOOK=1` is a Make‑friendly way to skip hook installation without needing a custom script.  
* **Separate `install-hook` target** – useful for CI pipelines or when the hook needs to be refreshed after edits.  

---  

## 3️⃣ `scripts/pre-commit` (the actual hook)