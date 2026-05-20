from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class ChangeType(enum.Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    ROLLED_BACK = "rolled_back"

class Severity(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ContractChangeEvent(Base):
    __tablename__ = 'contract_change_events'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String(255), nullable=False, index=True)
    change_type = Column(Enum(ChangeType), nullable=False, index=True)
    severity = Column(Enum(Severity), nullable=False, index=True)
    description = Column(Text, nullable=True)
    timestamp = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    metadata = Column(JSON, nullable=True)
    affected_contract_id = Column(String(255), nullable=False, index=True)
    change_author = Column(String(255), nullable=True)
    validation_status = Column(String(50), nullable=True, default="pending")