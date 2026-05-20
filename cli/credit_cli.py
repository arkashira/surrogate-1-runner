#!/usr/bin/env python3
"""Credit management CLI for axentx surrogate-1.
Provides commands to query and set credit balances with persistent storage.
"""
import os
import sys
import json
import click
from typing import Dict, Any

# Configuration
CREDIT_DATA_PATH = os.getenv("CREDIT_DATA_PATH", "/opt/axentx/surrogate-1/var/credit_balances.json")

def _load_balances() -> Dict[str, int]:
    """Load credit balances from persistent storage.
    Returns a dict with at least 'monthly' and 'bulk' keys.
    If storage is unavailable or malformed, returns default zero balances.
    """
    if not os.path.exists(CREDIT_DATA_PATH):
        return {"monthly": 0, "bulk": 0}

    try:
        with open(CREDIT_DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure required keys exist with default values
            data.setdefault("monthly", 0)
            data.setdefault("bulk", 0)
            return data
    except (json.JSONDecodeError, OSError):
        # Corrupt file or permission issues - reset to defaults
        return {"monthly": 0, "bulk": 0}

def _save_balances(balances: Dict[str, int]) -> None:
    """Persist credit balances to storage."""
    os.makedirs(os.path.dirname(CREDIT_DATA_PATH), exist_ok=True)
    with open(CREDIT_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(balances, f)

def get_status() -> Dict[str, Any]:
    """Get current credit status for both monthly and bulk balances."""
    balances = _load_balances()
    return {
        "monthly": {"balance": balances["monthly"]},
        "bulk": {"balance": balances["bulk"]}
    }

def set_bulk_credit(amount: int) -> Dict[str, Any]:
    """Set the bulk credit limit.
    Args:
        amount: The new bulk credit amount (must be non-negative).
    Returns:
        Dict with success status and updated balance.
    """
    if amount < 0:
        return {
            "success": False,
            "error": "Amount must be non-negative",
            "bulk": {"balance": _load_balances()["bulk"]}
        }

    balances = _load_balances()
    old_balance = balances["bulk"]
    balances["bulk"] = amount
    _save_balances(balances)

    return {
        "success": True,
        "message": f"Bulk credit limit updated from {old_balance} to {amount}",
        "bulk": {"balance": amount}
    }

@click.group()
def credit() -> None:
    """Credit management commands for axentx surrogate-1."""
    pass

@credit.command()
def status() -> None:
    """Return the current monthly and bulk credit balances as JSON."""
    result = get_status()
    click.echo(json.dumps(result, indent=2))
    return 0

@credit.command()
@click.argument("amount", type=int)
def set_bulk(amount: int) -> None:
    """Set the bulk credit limit.
    Example: credit set-bulk 5000
    """
    result = set_bulk_credit(amount)
    click.echo(json.dumps(result, indent=2))
    if not result.get("success", True):
        sys.exit(1)

if __name__ == "__main__":
    credit()