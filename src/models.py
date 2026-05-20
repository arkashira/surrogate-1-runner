from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class AccountCredit(Base):
    """
    One row per account.  Two independent credit buckets:
      * monthly – refreshed each calendar month
      * bulk    – long‑lived “pay‑as‑you‑go” pool
    """
    __tablename__ = "account_credit"

    account_id: Mapped[str] = mapped_column(sa.String, primary_key=True)

    # Totals are immutable from the service’s point of view;
    # they can be changed only by an admin operation (not shown here).
    monthly_total: Mapped[int] = mapped_column(sa.Integer, nullable=False, default=0)
    bulk_total: Mapped[int] = mapped_column(sa.Integer, nullable=False, default=0)

    # How much of each bucket has already been consumed.
    monthly_used: Mapped[int] = mapped_column(sa.Integer, nullable=False, default=0)
    bulk_used: Mapped[int] = mapped_column(sa.Integer, nullable=False, default=0)

    # --------------------------------------------------------------------- #
    # Helper methods
    # --------------------------------------------------------------------- #
    def to_dict(self) -> dict:
        """Serialise the row for API responses or tests."""
        return {
            "account_id": self.account_id,
            "monthly_total": self.monthly_total,
            "monthly_used": self.monthly_used,
            "bulk_total": self.bulk_total,
            "bulk_used": self.bulk_used,
        }

    @property
    def monthly_remaining(self) -> int:
        return max(self.monthly_total - self.monthly_used, 0)

    @property
    def bulk_remaining(self) -> int:
        return max(self.bulk_total - self.bulk_used, 0)

    @property
    def monthly_usage_pct(self) -> float:
        return (self.monthly_used / self.monthly_total * 100) if self.monthly_total else 0.0

    @property
    def bulk_usage_pct(self) -> float:
        return (self.bulk_used / self.bulk_total * 100) if self.bulk_total else 0.0