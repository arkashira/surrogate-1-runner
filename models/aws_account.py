"""
Simple in‑memory model for an AWS account integration.
In a real system this would be backed by an ORM / database.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Dict

__all__ = ["AwsAccount"]


@dataclass
class AwsAccount:
    """
    Represents an AWS account integration via an IAM role ARN.
    """

    account_id: str
    role_arn: str
    name: str = field(default="")

    # In‑memory store keyed by account_id
    _store: ClassVar[Dict[str, "AwsAccount"]] = {}

    @classmethod
    def create(cls, account_id: str, role_arn: str, name: str = "") -> "AwsAccount":
        """
        Persist a new account.  Raises ValueError if the ID already exists.
        """
        if account_id in cls._store:
            raise ValueError(f"Account {account_id} already exists")
        account = cls(account_id=account_id, role_arn=role_arn, name=name)
        cls._store[account_id] = account
        return account

    @classmethod
    def get(cls, account_id: str) -> "AwsAccount":
        """Retrieve an account by ID. Raises KeyError if not found."""
        return cls._store[account_id]

    @classmethod
    def list(cls) -> Dict[str, "AwsAccount"]:
        """Return a copy of all stored accounts."""
        return dict(cls._store)