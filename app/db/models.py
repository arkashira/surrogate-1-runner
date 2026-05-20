from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, JSON, DateTime
from . import Base

class SimulationResult(Base):
    __tablename__ = "simulation_results"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    estimated_revenue = Column(Float, nullable=False)
    conversion_rate = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)