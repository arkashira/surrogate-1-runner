"""
Stripe Transaction Model - Synthesized from best practices.
Uses Integer for amount (cents) to avoid floating-point precision issues.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class StripeTransaction(Base):
    """
    Represents a single Stripe charge or payment intent.
    Stores amount in cents as Integer for financial precision.
    """
    
    __tablename__ = "stripe_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stripe_id = Column(String(255), unique=True, nullable=False, index=True)
    amount = Column(Integer, nullable=False)  # Amount in CENTS - critical for precision
    currency = Column(String(3), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String(50), nullable=False)
    customer_id = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    receipt_url = Column(String(500), nullable=True)
    metadata_json = Column(Text, nullable=True)  # Store additional metadata as JSON

    def __repr__(self):
        return f"<StripeTransaction(id={self.id}, stripe_id='{self.stripe_id}', amount={self.amount})>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "stripe_id": self.stripe_id,
            "amount": self.amount,
            "currency": self.currency,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "status": self.status,
            "customer_id": self.customer_id,
            "description": self.description,
            "receipt_url": self.receipt_url,
        }