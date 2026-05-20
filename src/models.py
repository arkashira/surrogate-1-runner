from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ComplianceFinding(Base):
    __tablename__ = "compliance_findings"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(String(255), nullable=False)
    resource_type = Column(String(255), nullable=False)
    rule_id = Column(String(255), nullable=False)
    rule_name = Column(String(255), nullable=False)
    severity = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    detected_at = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    status = Column(String(50), nullable=False, server_default="open")
    resolved_at = Column(DateTime)