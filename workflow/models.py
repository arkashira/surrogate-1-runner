from datetime import datetime
from typing import List

from sqlalchemy import Column, String, DateTime, PickleType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Workflow(Base):
    __tablename__ = 'workflows'

    id = Column(String, primary_key=True)
    name = Column(String)
    steps = Column(PickleType)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Workflow {self.id}: {self.name}>'