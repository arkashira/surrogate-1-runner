from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Tuple

from jsonschema import Draft7Validator, ValidationError

# --------------------------------------------------------------------------- #
# Configuration (can be overridden by env vars in production)
# --------------------------------------------------------------------------- #
CONTRACTS_DIR: Path = Path(
    os.getenv("CONTRACTS_DIR", "/opt/axentx/surrogate-1/contracts")
).resolve()
LATENCY_BUDGET_MS: float = float(os.getenv("LATENCY_BUDGET_MS", "50"))

# --------------------------------------------------------------------------- #
# Internal cache – one entry per (job, direction)
# --------------------------------------------------------------------------- #
_schema_cache: Dict[Tuple[str, str], Draft7Validator] = {}


def _load_validator(job: str, direction: str) -> Draft7Validator:
    """
    Load (and cache) a Draft‑7 JSON‑Schema validator for a given job.

    Parameters
    ----------
    job: str
        The logical name of the async job (e.g. ``sample_job``).
    direction: str
        Either ``"request"`` or ``"response"``.

    Returns
    -------
    Draft7Validator
        A compiled validator ready for ``iter_errors``.

    Raises
    ------
    FileNotFoundError
        If the expected ``<job>_<direction>.json`` file does not exist.
    json.JSONDecodeError
        If the schema file is not valid JSON.
    """
    cache_key = (job, direction)
    if cache_key in _schema_cache:
        return _schema_cache[cache_key]

    schema_path = CONTRACTS_DIR / f"{job}_{direction}.json"
    if not schema_path.is_file():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    validator = Draft7Validator(schema)
    _schema_cache[cache_key] = validator
    return validator


def _first_error(instance: Any, validator: Draft7Validator) -> ValidationError | None:
    """
    Return the first validation error (sorted by JSON‑pointer path) or ``None``.
    """
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
    return errors[0] if errors else None


def validate_job(
    job: str,
    request_payload: Any,
    response_payload: Any,
) -> Tuple[bool, str]:
    """
    Validate *both* request and response payloads for a given job.

    The function is deliberately **side‑effect free** – it never prints or raises
    (except for unrecoverable I/O errors).  Instead it returns a tuple:

    ``(True, "")``                     – everything matches and latency < budget  
    ``(False, "<human‑readable reason>")`` – validation failed or latency exceeded

    Parameters
    ----------
    job: str
        Identifier that matches the schema file prefix.
    request_payload, response_payload: Any
        JSON‑serialisable Python objects (dict, list, primitives).

    Returns
    -------
    Tuple[bool, str]
        ``bool`` indicates success, ``str`` contains an error message when
        ``bool`` is ``False``.
    """
    start = time.perf_counter()

    # 1️⃣ Validate request
    try:
        req_validator = _load_validator(job, "request")
    except Exception as exc:  # FileNotFoundError, JSONDecodeError, etc.
        return False, f"Unable to load request schema: {exc}"

    err = _first_error(request_payload, req_validator)
    if err:
        return False, f"Request validation error: {err.message} (path: {'/'.join(map(str, err.path))})"

    # 2️⃣ Validate response
    try:
        resp_validator = _load_validator(job, "response")
    except Exception as exc:
        return False, f"Unable to load response schema: {exc}"

    err = _first_error(response_payload, resp_validator)
    if err:
        return False, f"Response validation error: {err.message} (path: {'/'.join(map(str, err.path))})"

    # 3️⃣ Latency guard
    elapsed_ms = (time.perf_counter() - start) * 1000
    if elapsed_ms > LATENCY_BUDGET_MS:
        return (
            False,
            f"Validation latency {elapsed_ms:.2f} ms exceeds budget of {LATENCY_BUDGET_MS} ms",
        )

    return True, ""  # success