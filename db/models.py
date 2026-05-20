from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class SubscriptionPlan(enum.Enum):
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class SubscriptionStatus(enum.Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"

class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    stripe_subscription_id = Column(String, unique=True, nullable=True)
    plan = Column(Enum(SubscriptionPlan), nullable=False)
    max_concurrent_streams = Column(Integer, nullable=False)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ends_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    
    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, plan={self.plan})>"

class ApiKey(Base):
    __tablename__ = 'api_keys'
    
    id = Column(Integer, primary_key=True, index=True)
    key_hash = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'), nullable=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")
    subscription = relationship("Subscription", back_populates="api_keys")
    
    def __repr__(self):
        return f"<ApiKey(id={self.id}, name={self.name}, is_active={self.is_active})>"