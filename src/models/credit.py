"""
Credit model for tracking user monthly and bulk credits.
"""
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Credit(Base):
    """
    Stores monthly and bulk credit balances per user.
    """
    __tablename__ = 'credits'
    __table_args__ = (
        UniqueConstraint('user_id', name='uq_credits_user_id'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    monthly_credits = Column(Integer, nullable=False, default=0)
    bulk_credits = Column(Integer, nullable=False, default=0)
    last_monthly_reset = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to user
    user = relationship("User", back_populates="credits")
    
    @property
    def total_credits(self) -> int:
        """Total available credits (monthly + bulk)."""
        return self.monthly_credits + self.bulk_credits
    
    def can_deduct(self, amount: int = 1) -> bool:
        """Check if user has enough credits."""
        return self.total_credits >= amount
    
    def deduct(self, amount: int = 1) -> bool:
        """
        Deduct from monthly credits first, then bulk credits.
        
        Args:
            amount: Number of credits to deduct
            
        Returns:
            True if deduction successful, False if insufficient credits
        """
        if not self.can_deduct(amount):
            return False
        
        remaining = amount
        
        # Deduct from monthly first
        if self.monthly_credits >= remaining:
            self.monthly_credits -= remaining
        else:
            remaining -= self.monthly_credits
            self.monthly_credits = 0
            # Deduct remaining from bulk
            self.bulk_credits -= remaining
        
        self.updated_at = datetime.utcnow()
        return True
    
    def reset_monthly(self, default_amount: int) -> None:
        """Reset monthly credits to default amount."""
        self.monthly_credits = default_amount
        self.last_monthly_reset = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def add_bulk(self, amount: int) -> None:
        """Add bulk credits to user account."""
        if amount <= 0:
            raise ValueError("Bulk credit amount must be positive")
        self.bulk_credits += amount
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Return dictionary representation."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'monthly_credits': self.monthly_credits,
            'bulk_credits': self.bulk_credits,
            'total_credits': self.total_credits,
            'last_monthly_reset': self.last_monthly_reset.isoformat() if self.last_monthly_reset else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


# Import User type for type hints only (avoids circular import)
if TYPE_CHECKING:
    from models.user import User