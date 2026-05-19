from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from .database import Base
import enum


class DealStatus(enum.Enum):
    PENDING = "Pending"
    ACTIVE = "Active"
    DEAL_CLOSED = "Deal Closed"
    CANCELLED = "Cancelled"


class UserRole(enum.Enum):
    PROVIDER = "Provider"
    INVESTOR = "Investor"
    ADMIN = "Admin"


class User(Base):
    """Unified user model for both providers and investors."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True, server_default=expression.true())
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    provider_feedbacks = relationship("Feedback", foreign_keys="Feedback.provider_id", back_populates="provider")
    investor_feedbacks = relationship("Feedback", foreign_keys="Feedback.investor_id", back_populates="investor")
    given_deals = relationship("Deal", foreign_keys="Deal.investor_id", back_populates="investor")
    received_deals = relationship("Deal", foreign_keys="Deal.provider_id", back_populates="provider")


class Deal(Base):
    """Deal model linking providers and investors."""
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    investor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(DealStatus), default=DealStatus.PENDING)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    closed_at = Column(DateTime, nullable=True)

    # Relationships
    provider = relationship("User", foreign_keys=[provider_id], back_populates="received_deals")
    investor = relationship("User", foreign_keys=[investor_id], back_populates="given_deals")


class Feedback(Base):
    """Feedback model for investor-provider ratings."""
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    investor_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)  # 1-5 scale
    comment = Column(Text, nullable=True)
    is_approved = Column(Boolean, default=False, server_default=expression.false())  # For moderation
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    provider = relationship("User", foreign_keys=[provider_id], back_populates="provider_feedbacks")
    investor = relationship("User", foreign_keys=[investor_id], back_populates="investor_feedbacks")

    # Composite index for efficient queries
    __table_args__ = (
        Index('idx_provider_investor', 'provider_id', 'investor_id'),
    )


# Add missing import
from sqlalchemy import Index, Boolean