"""
SQLAlchemy models for the matching service.
"""

from datetime import datetime
from typing import List

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Table,
    Boolean,
    create_engine,
    MetaData,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

# --------------------------------------------------------------------------- #
# Engine / Session
# --------------------------------------------------------------------------- #

# In production this would be a real database URL.
# For the demo we use SQLite in a file so that the data survives rest‑arts.
DATABASE_URL = "sqlite:///matching.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

# --------------------------------------------------------------------------- #
# Base
# --------------------------------------------------------------------------- #

Base = declarative_base()

# --------------------------------------------------------------------------- #
# Models
# --------------------------------------------------------------------------- #

class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # Tags are stored as a comma‑separated string for SQLite compatibility.
    tags = Column(String, nullable=False)  # e.g. "fintech,series_a,ny"

    def tag_set(self) -> set[str]:
        return {t.strip().lower() for t in self.tags.split(",") if t}

    def __repr__(self) -> str:
        return f"<Provider id={self.id} name={self.name}>"


class Investor(Base):
    __tablename__ = "investors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tags = Column(String, nullable=False)  # e.g. "fintech,series_a,ny"
    active = Column(Boolean, default=True, nullable=False)

    def tag_set(self) -> set[str]:
        return {t.strip().lower() for t in self.tags.split(",") if t}

    def __repr__(self) -> str:
        return f"<Investor id={self.id} name={self.name}>"


class MatchAudit(Base):
    """
    Persist every match that the service produces.
    """
    __tablename__ = "match_audit"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, nullable=False)
    investor_id = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<MatchAudit provider={self.provider_id} "
            f"investor={self.investor_id} score={self.score:.3f}>"
        )


# --------------------------------------------------------------------------- #
# Utility
# --------------------------------------------------------------------------- #

def init_db() -> None:
    """
    Create all tables.  In a real project you would use Alembic migrations.
    """
    Base.metadata.create_all(bind=engine)


def get_session():
    """
    Return a thread‑local scoped session.
    """
    return SessionLocal()