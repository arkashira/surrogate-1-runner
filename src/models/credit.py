from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock
from typing import Dict, Optional


@dataclass(frozen=True)
class CreditBalance:
    """
    Immutable representation of a user’s credit balances.

    Validation is performed in ``__post_init__`` so that no instance can ever
    contain a negative value – this guarantees data integrity throughout the
    stack.
    """
    bulk_balance: float = field(metadata={"description": "Total bulk credits"})
    monthly_balance: float = field(metadata={"description": "Credits available this month"})

    def __post_init__(self) -> None:
        if self.bulk_balance < 0:
            raise ValueError("Bulk balance cannot be negative")
        if self.monthly_balance < 0:
            raise ValueError("Monthly balance cannot be negative")


class CreditService:
    """
    Simple in‑memory credit store with thread‑safety.

    In production you would replace the ``_store`` implementation with a real
    persistence layer (SQL, NoSQL, Redis, …) while keeping the public API
    unchanged.
    """

    def __init__(self) -> None:
        # ``_store`` maps ``user_id`` → ``CreditBalance``.
        self._store: Dict[str, CreditBalance] = {}
        self._lock = RLock()               # protects concurrent reads/writes

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def get_balance(self, user_id: str) -> CreditBalance:
        """
        Return the current balance for *user_id*.
        If the user does not exist, a zero‑balance object is returned
        (this mirrors the “default balance” behaviour from the drafts).
        """
        with self._lock:
            return self._store.get(user_id, CreditBalance(0.0, 0.0))

    def set_balance(
        self,
        user_id: str,
        *,
        bulk_balance: Optional[float] = None,
        monthly_balance: Optional[float] = None,
    ) -> CreditBalance:
        """
        Create or replace a user’s balance.

        Parameters
        ----------
        user_id: str
            Identifier of the user.
        bulk_balance: float | None
            New bulk balance. If ``None`` the existing bulk balance is kept.
        monthly_balance: float | None
            New monthly balance. If ``None`` the existing monthly balance is kept.

        Returns
        -------
        CreditBalance
            The freshly stored balance (useful for the API response).
        """
        with self._lock:
            current = self._store.get(user_id, CreditBalance(0.0, 0.0))

            new_bulk = bulk_balance if bulk_balance is not None else current.bulk_balance
            new_monthly = monthly_balance if monthly_balance is not None else current.monthly_balance

            # Validation happens inside CreditBalance
            new_balance = CreditBalance(bulk_balance=new_bulk, monthly_balance=new_monthly)
            self._store[user_id] = new_balance
            return new_balance

    def adjust_balance(
        self,
        user_id: str,
        *,
        bulk_delta: float = 0.0,
        monthly_delta: float = 0.0,
    ) -> CreditBalance:
        """
        Atomically add/subtract amounts from a user’s balance.

        Raises
        ------
        ValueError
            If the resulting balance would be negative.
        """
        with self._lock:
            current = self.get_balance(user_id)
            return self.set_balance(
                user_id,
                bulk_balance=current.bulk_balance + bulk_delta,
                monthly_balance=current.monthly_balance + monthly_delta,
            )

    # --------------------------------------------------------------------- #
    # Helper for testing / migrations
    # --------------------------------------------------------------------- #
    def _reset(self) -> None:
        """Clear the in‑memory store – useful for unit tests."""
        with self._lock:
            self._store.clear()


# A module‑level singleton that the API layer can import.
credit_service = CreditService()