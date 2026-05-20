from sqlalchemy import Column, Integer, String, JSON, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Component(Base):
    __tablename__ = 'components'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    manufacturer = Column(String(100))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    # Benchmark fields per PRD 20260503-081816-reddit-0a3d688046dde7a4
    benchmark_scores = Column(JSON, nullable=True)  # Stores PassMark, UserBenchmark, Geekbench
    composite_score = Column(Float, nullable=True)  # Normalized weekly-updated composite