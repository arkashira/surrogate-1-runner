from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Interaction(Base):
    """
    Represents an interaction between an investor and a provider.
    A status field has been added to track the current state of the
    interaction (e.g., 'In Review', 'Rejected', 'Deal Closed').
    """
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    investor_id = Column(Integer, ForeignKey("investors.id"), nullable=False)

    # Existing fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # New status field
    status = Column(
        String(32),
        nullable=False,
        default="Pending",
        comment="Current status of the interaction",
    )

    # Relationships
    provider = relationship("Provider", back_populates="interactions")
    investor = relationship("Investor", back_populates="interactions")

    def __repr__(self) -> str:
        return (
            f"<Interaction id={self.id} provider_id={self.provider_id} "
            f"investor_id={self.investor_id} status={self.status}>"
        )