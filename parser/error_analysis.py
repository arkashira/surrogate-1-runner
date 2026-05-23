"""
Error analysis and recovery utilities for the surrogate-1 parser.

This module provides:
* A decorator `recoverable` that wraps parsing functions to catch common
  parsing errors, log them with context, and return `None` for the failed
  record instead of raising.
* Helper functions to identify, log, and attempt simple recovery from
  common errors such as missing keys, type mismatches, and malformed JSON.
* A small recovery strategy that can be extended by the caller.

The goal is to allow the parser to continue processing a stream of
records without losing the rest of the data.
"""

import json
import logging
import re
from functools import wraps
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, TypeVar

# Configure a module-level logger. In production this should be
# configured by the application entry point, but we provide a sane
# default for tests and standalone usage.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

T = TypeVar("T")


# --------------------------------------------------------------------------- #
# Common error identification utilities
# --------------------------------------------------------------------------- #
def identify_error(e: Exception) -> str:
    """
    Return a human‑readable description of the error type.
    """
    if isinstance(e, json.JSONDecodeError):
        return "Malformed JSON"
    if isinstance(e, KeyError):
        return f"Missing key: {e.args[0]}"
    if isinstance(e, ValueError):
        return f"Value error: {e}"
    if isinstance(e, TypeError):
        return f"Type error: {e}"
    return f"Unhandled exception: {type(e).__name__}"


def log_error(e: Exception, context: Optional[Dict[str, Any]] = None) -> None:
    """
    Log the error with context information.
    """
    msg = f"Parsing error: {identify_error(e)}"
    if context:
        msg += f" | Context: {context}"
    logger.error(msg, exc_info=e)


# --------------------------------------------------------------------------- #
# Recovery strategies
# --------------------------------------------------------------------------- #
def recover_missing_key(data: Dict[str, Any], key: str, default: Any = None) -> Dict[str, Any]:
    """
    If a required key is missing, insert a default value.
    """
    if key not in data:
        logger.warning(f"Missing key '{key}'. Inserting default value: {default}")
        data[key] = default
    return data


def recover_type_mismatch(value: Any, expected_type: type, default: Any = None) -> Any:
    """
    Attempt to coerce a value to the expected type. If coercion fails,
    return a default.
    """
    try:
        return expected_type(value)
    except Exception:
        logger.warning(
            f"Type mismatch: cannot convert {value!r} to {expected_type.__name__}. "
            f"Using default {default!r}"
        )
        return default


# --------------------------------------------------------------------------- #
# Decorator for recoverable parsing functions
# --------------------------------------------------------------------------- #
def recoverable(parser_func: Callable[..., T]) -> Callable[..., Optional[T]]:
    """
    Decorator that wraps a parsing function to catch common errors,
    log them, and return None instead of propagating the exception.

    The wrapped function should accept a single argument `record` (dict)
    and return a parsed object or raise an exception on failure.
    """

    @wraps(parser_func)
    def wrapper(record: Dict[str, Any]) -> Optional[T]:
        try:
            return parser_func(record)
        except Exception as e:
            log_error(e, context={"record_id": record.get("id")})
            # Attempt simple recovery for known error types
            if isinstance(e, KeyError):
                # Insert missing key with None and retry
                missing_key = e.args[0]
                record = recover_missing_key(record, missing_key)
                try:
                    return parser_func(record)
                except Exception as retry_e:
                    log_error(retry_e, context={"record_id": record.get("id")})
            elif isinstance(e, ValueError):
                # Try to coerce problematic fields if possible
                # (Assuming parser_func uses a known schema; this is a placeholder)
                pass
            # If recovery fails, return None to signal a skipped record
            return None

    return wrapper


# --------------------------------------------------------------------------- #
# Example usage: process a stream of records
# --------------------------------------------------------------------------- #
def process_records(
    records: Iterable[Dict[str, Any]],
    parser_func: Callable[[Dict[str, Any]], T],
) -> List[Tuple[Optional[T], Dict[str, Any]]]:
    """
    Process an iterable of raw records, applying the parser_func to each.
    Returns a list of tuples (parsed_object_or_None, original_record).
    Records that fail to parse are logged and skipped (None returned).
    """
    wrapped_parser = recoverable(parser_func)
    results: List[Tuple[Optional[T], Dict[str, Any]]] = []

    for record in records:
        parsed = wrapped_parser(record)
        results.append((parsed, record))

    return results