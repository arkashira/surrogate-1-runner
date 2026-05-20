import time
from sqlalchemy import Column, Integer, Float, String, JSON, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SimulationResult(Base):
    __tablename__ = "simulation_result"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    payload = Column(JSON, nullable=False)
    results = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: time.time(), index=True)