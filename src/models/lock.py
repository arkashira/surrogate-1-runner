from datetime import datetime, timedelta
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Lock(Base):
    __tablename__ = 'locks'

    id = Column(String, primary_key=True)
    doc_id = Column(String, nullable=False)
    section_id = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=2))
    ttl = Column(Integer, default=7200)  # 2 hours in seconds