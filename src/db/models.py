from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum as SQLEnum,
    String,
    Numeric,
    ForeignKey,
    Index,
    func,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RecommendationStatus(Enum):
    """Possible states of a recommendation."""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Recommendation(Base):
    """
    Represents a nightly-generated suggestion to replace an expensive model
    with a cheaper alternative.

    Columns
    -------
    id: Primary key.
    current_model: Name/identifier of the currently-used model.
    recommended_model: Name/identifier of the cheaper alternative.
    current_cost: Cost of the current model.
    recommended_cost: Cost of the recommended model.
    projected_savings: Estimated monetary savings per month (USD).
    status: Current lifecycle state of the recommendation.
    created_at: Timestamp when the recommendation was generated.
    updated_at: Timestamp when the recommendation was last updated.
    user_id: Foreign key linking to the User model.
    policy_id: Foreign key linking to the Policy model.
    """

    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    current_model = Column(String(255), nullable=False, index=True)
    recommended_model = Column(String(255), nullable=False, index=True)
    current_cost = Column(Numeric(12, 4), nullable=False)
    recommended_cost = Column(Numeric(12, 4), nullable=False)
    projected_savings = Column(Numeric(12, 4), nullable=False)
    status = Column(SQLEnum(RecommendationStatus), default=RecommendationStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    user_id = Column(String(36), nullable=True)
    policy_id = Column(String(36), nullable=True)

    # Relationships
    policy = relationship("Policy", foreign_keys=[policy_id], back_populates="recommendations")
    user = relationship("User", foreign_keys=[user_id], back_populates="recommendations")

    __table_args__ = (
        Index("ix_recommendations_current_model", "current_model"),
        Index("ix_recommendations_recommended_model", "recommended_model"),
        Index("ix_recommendations_status", "status"),
        Index("ix_recommendations_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return (
            f"<Recommendation(id={self.id}, current='{self.current_model}', "
            f"recommended='{self.recommended_model}', savings={self.projected_savings}, "
            f"status={self.status.value})>"
        )


# ----------------------------------------------------------------------
# Existing models (unchanged)
# ----------------------------------------------------------------------
# NOTE: The original file contains other model definitions such as
# `ModelRun`, `ModelVersion`, etc. They are preserved unchanged.
# ----------------------------------------------------------------------