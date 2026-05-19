from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app import db  # assumes Flask‑SQLAlchemy or similar

class Interaction(db.Model):
    __tablename__ = 'interactions'

    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey('providers.id'), nullable=False)
    investor_id = Column(Integer, ForeignKey('investors.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    interaction_type = Column(String(50), nullable=False)

    provider = relationship(
        "Provider",
        back_populates="interactions",
        foreign_keys=[provider_id]
    )
    investor = relationship(
        "Investor",
        back_populates="interactions",
        foreign_keys=[investor_id]
    )