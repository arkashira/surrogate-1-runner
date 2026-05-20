from sqlalchemy import Column, Integer, String, Float, Decimal, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CPU(Base):
    __tablename__ = 'cpus'
    
    id = Column(Integer, primary_key=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    cores = Column(Integer, nullable=False)
    threads = Column(Integer, nullable=False)
    base_clock = Column(Float, nullable=False)
    boost_clock = Column(Float, nullable=False)
    cache = Column(Integer, nullable=False)  # in MB
    tdp = Column(Integer, nullable=False)    # in watts
    price = Column(Decimal(10,2), nullable=False)
    performance_score = Column(Integer, nullable=False)  # synthetic benchmark score
    
    __table_args__ = (
        Index('idx_cpu_brand', 'brand'),
        Index('idx_cpu_price', 'price'),
        Index('idx_cpu_performance', 'performance_score'),
    )