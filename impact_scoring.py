#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Impact Scoring Service
======================

A FastAPI application that scores audit findings on a 0‑100 scale.

Features
--------
* **Async** – FastAPI + uvicorn for high throughput.
* **Thread‑safe in‑memory store** – satisfies the 5‑second update requirement.
* **Background scoring** – POST is instant; scoring happens in the background.
* **OpenAPI docs** – `/docs` and `/redoc`.
* **Logging** – structured, JSON‑friendly logs.
* **Unit‑test friendly** – `ImpactScoringEngine` is pure and testable.

Run
---