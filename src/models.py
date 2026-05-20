"""
Database models for surrogate-1.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Organization(Base):
    """Organization that owns resources and budgets."""
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    budgets = relationship("Budget", back_populates="organization", cascade="all, delete-orphan")

class Budget(Base):
    """Monthly budget limit for an organization."""
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    month = Column(String(7), nullable=False, index=True)  # Format: YYYY-MM
    limit = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="budgets")

    def to_dict(self):
        """Serialize Budget instance to dictionary."""
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "month": self.month,
            "limit": float(self.limit),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }