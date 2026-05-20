"""
Match model for provider‑investor matching.

The model mirrors the migration above and adds a few niceties:
* `meets_threshold` – a property that tells you if the match is worth
  surfacing (score >= 70).
* `to_dict()` – serialises the row for API responses or background jobs.
"""

from datetime import datetime
from typing import Any, Dict

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, autoincrement=True)

    provider_id = Column(
        Integer,
        ForeignKey("providers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    investor_id = Column(
        Integer,
        ForeignKey("investors.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # 0‑100 score – stored as an integer for precision and size
    score = Column(Integer, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    # ORM relationships – optional but handy for eager loading
    provider = relationship("Provider", back_populates="matches")
    investor = relationship("Investor", back_populates="matches")

    # Constraints & indexes that mirror the migration
    __table_args__ = (
        CheckConstraint(
            "score >= 0 AND score <= 100",
            name="match_score_range_check",
        ),
        UniqueConstraint(
            "provider_id",
            "investor_id",
            name="unique_provider_investor_pair",
        ),
        Index("idx_matches_score", "score"),
        Index("idx_matches_created_at", "created_at"),
    )

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------
    @property
    def meets_threshold(self) -> bool:
        """Return True if the match score is >= 70."""
        return self.score >= 70

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON‑serialisable dict representation."""
        return {
            "id": self.id,
            "provider_id": self.provider_id,
            "investor_id": self.investor_id,
            "score": self.score,
            "created_at": self.created_at.isoformat()
            if self.created_at
            else None,
        }

    def __repr__(self) -> str:
        return (
            f"<Match(id={self.id}, provider_id={self.provider_id}, "
            f"investor_id={self.investor_id}, score={self.score})>"
        )