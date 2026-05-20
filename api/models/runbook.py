"""
SQLAlchemy model for a Runbook.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Text

from ..database import Base


class Runbook(Base):
    __tablename__ = "runbooks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String, nullable=True)  # Comma-separated for simplicity
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)