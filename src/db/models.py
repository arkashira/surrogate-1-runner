from sqlalchemy import Column, String, Date, Numeric, JSON, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Index

Base = declarative_base()

class CostinelSnapshot(Base):
    __tablename__ = 'costinel_monthly_snapshot'
    
    tenant_id = Column(String(36), primary_key=True)
    snapshot_date = Column(Date, primary_key=True)
    total_spend = Column(Numeric(15,2), nullable=False)
    service_breakdown = Column(MutableDict.as_mutable(JSONB), nullable=False)
    savings_recommendations = Column(MutableDict.as_mutable(JSONB), nullable=False)
    fetched_at = Column(DateTime(timezone=False), nullable=False, server_default='NOW()')
    
    __table_args__ = (
        Index('idx_costinel_snapshot_fetched', 'fetched_at'),
        Index('idx_costinel_service_breakdown_gin', 'service_breakdown', postgresql_using='gin'),
        Index('idx_costinel_savings_gin', 'savings_recommendations', postgresql_using='gin')
    )