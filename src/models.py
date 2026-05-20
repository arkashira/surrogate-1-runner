"""
Database models for surrogate‑1.
"""
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Text,
    Index,
    Numeric,          # <-- new import
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Run(Base):
    """Represents a single worker run."""
    __tablename__ = 'runs'

    id = Column(Integer, primary_key=True)
    worker_id = Column(String(64), nullable=False, index=True)
    shard_id = Column(Integer, nullable=False, index=True)
    status = Column(String(32), nullable=False, default='pending')
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # ------------------------------------------------------------------
    # NEW: cost of the run (USD).  Numeric gives exact decimal arithmetic,
    #       10 total digits with 2 after the decimal point → max $99,999,999.99
    # ------------------------------------------------------------------
    cost = Column(
        Numeric(10, 2),          # precision, scale
        nullable=True,
        doc="Cost in USD reported by the provider API"
    )

    error_message = Column(Text, nullable=True)

    __table_args__ = (
        Index('idx_worker_status', 'worker_id', 'status'),
        Index('idx_shard_status', 'shard_id', 'status'),
    )

    def __repr__(self):
        return (
            f"<Run(id={self.id}, worker_id={self.worker_id}, "
            f"shard_id={self.shard_id}, status={self.status}, cost={self.cost})>"
        )


class Shard(Base):
    """Represents a dataset shard."""
    __tablename__ = 'shards'

    id = Column(Integer, primary_key=True)
    shard_id = Column(Integer, nullable=False, unique=True, index=True)
    total_runs = Column(Integer, nullable=False, default=0)
    completed_runs = Column(Integer, nullable=False, default=0)
    last_run_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return (
            f"<Shard(shard_id={self.shard_id}, "
            f"completed={self.completed_runs}/{self.total_runs})>"
        )