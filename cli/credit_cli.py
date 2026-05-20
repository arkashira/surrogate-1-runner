#!/usr/bin/env python3
"""
Credit management CLI for surrogate-1.

Provides commands to query and set credit balances:
  credit status          - Returns current monthly and bulk balances in JSON
  credit set-bulk <amount> - Updates the bulk credit limit
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class CreditBalances:
    """Credit balance data structure."""
    monthly: int
    bulk: int
    
    def to_dict(self) -> dict:
        return asdict(self)


class CreditStore:
    """
    In-memory credit balance storage.
    
    Note: In production, this should be backed by persistent storage
    (database, config file, or environment variables).
    """
    
    def __init__(self, monthly: int = 1000, bulk: int = 5000):
        self._monthly = monthly
        self._bulk = bulk
    
    def get_balances(self) -> CreditBalances:
        """Retrieve current credit balances."""
        return CreditBalances(monthly=self._monthly, bulk=self._bulk)
    
    def set_bulk(self, amount: int) -> CreditBalances:
        """Update bulk credit limit."""
        if amount < 0:
            raise ValueError("Bulk amount cannot be negative")
        self._bulk = amount
        return self.get_balances()


# Global store instance
_credit_store = CreditStore()


def status_command(args) -> int:
    """Execute the credit status command."""
    try:
        balances = _credit_store.get_balances()
        output = {
            "success": True,
            "balances": balances.to_dict()
        }
        print(json.dumps(output, indent=2))
        return 0
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, indent=2), file=sys.stderr)
        return 1


def set_bulk_command(args) -> int:
    """Execute the credit set-bulk command."""
    try:
        amount = int(args.amount)
        balances = _credit_store.set_bulk(amount)
        output = {
            "success": True,
            "message": f"Bulk credit limit updated to {amount}",
            "balances": balances.to_dict()
        }
        print(json.dumps(output, indent=2))
        return 0
    except ValueError as e:
        print(json.dumps({"success": False, "error": f"Invalid amount: {e}"}, indent=2), file=sys.stderr)
        return 1
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, indent=2), file=sys.stderr)
        return 1


def main(argv: Optional[list] = None) -> int:
    """Main entry point for the credit CLI."""
    parser = argparse.ArgumentParser(
        prog="credit",
        description="Manage credit balances"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Status subcommand
    subparsers.add_parser("status", help="Show current credit balances")
    
    # Set-bulk subcommand
    set_bulk_parser = subparsers.add_parser("set-bulk", help="Set bulk credit limit")
    set_bulk_parser.add_argument("amount", type=int, help="New bulk credit amount")
    
    args = parser.parse_args(argv)
    
    if args.command == "status":
        return status_command(args)
    elif args.command == "set-bulk":
        return set_bulk_command(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())