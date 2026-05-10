"""
SQLAlchemy ORM model for a diagnostic session.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DiagnosticSession(Base):
    """Represents a single diagnostic session captured via the REST API."""

    __tablename__ = "diagnostic_sessions"

    diagnostic_session_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    device_id = Column(String(255), nullable=False)
    error_code = Column(String(50), nullable=False)
    error_message = Column(String(1024), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    protocol_version = Column(String(50), nullable=False)

    def __repr__(self) -> str:
        return (
            f"<DiagnosticSession(id={self.diagnostic_session_id!s}, "
            f"device_id={self.device_id!r}, error_code={self.error_code!r})>"
        )