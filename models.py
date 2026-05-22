from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Index,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Signature(Base):
    __tablename__ = "signatures"

    service = Column(String(255), nullable=False)
    version = Column(String(100), nullable=False)
    signature_hash = Column(Text, nullable=False)   # encrypted blob
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("service", "version", name="uq_service_version"),
        Index("ix_signatures_service", "service"),
        Index("ix_signatures_created_at", "created_at"),
    )