from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Finding(Base):
    __tablename__ = 'findings'

    id = Column(Integer, primary_key=True)
    resource_id = Column(String, nullable=False)
    rule_name = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    dashboard_link = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

class AlertLog(Base):
    __tablename__ = 'alert_logs'

    id = Column(Integer, primary_key=True)
    finding_id = Column(Integer, ForeignKey('findings.id'), nullable=False)
    delivered_at = Column(DateTime, nullable=False)
    success = Column(Boolean, nullable=False)

    finding = relationship("Finding", back_populates="alert_logs")

class MutedRule(Base):
    __tablename__ = 'muted_rules'

    id = Column(Integer, primary_key=True)
    rule_name = Column(String, nullable=False)