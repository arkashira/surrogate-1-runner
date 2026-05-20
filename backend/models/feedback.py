"""
Feedback model for investor ratings on provider profiles.

After an investor marks a match 'Deal Closed', they can leave a 1-5 star rating
and optional comment. Each investor-provider pair can only submit one feedback.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Feedback(Base):
    """
    Represents investor feedback for a provider after a 'Deal Closed' match.
    
    Constraints:
        - One feedback per investor-provider pair (enforced by unique constraint)
        - Rating must be 1-5 stars
        - Comment is optional
    """
    __tablename__ = 'feedback'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign keys with cascade delete
    provider_id = Column(
        Integer,
        ForeignKey('providers.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        doc='Reference to the provider receiving feedback'
    )
    
    investor_id = Column(
        Integer,
        ForeignKey('investors.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        doc='Reference to the investor giving feedback'
    )
    
    # Feedback content
    rating = Column(
        Integer,
        nullable=False,
        doc='Rating from 1-5 stars'
    )
    
    comment = Column(
        Text,
        nullable=True,
        doc='Optional comment from the investor'
    )
    
    # Timestamps
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        doc='Timestamp when feedback was submitted'
    )
    
    # Unique constraint: one feedback per investor-provider pair
    __table_args__ = (
        UniqueConstraint('investor_id', 'provider_id', name='uq_feedback_investor_provider'),
    )
    
    # Relationships
    provider = relationship("Provider", back_populates="feedback_received", foreign_keys=[provider_id])
    investor = relationship("Investor", back_populates="feedback_given", foreign_keys=[investor_id])
    
    def __repr__(self):
        return f"<Feedback(id={self.id}, provider_id={self.provider_id}, investor_id={self.investor_id}, rating={self.rating})>"
    
    def to_dict(self):
        """Convert feedback to dictionary for API responses."""
        return {
            'id': self.id,
            'provider_id': self.provider_id,
            'investor_id': self.investor_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }