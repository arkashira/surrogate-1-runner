from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

Base = declarative_base()

class AWSResource(Base):
    __tablename__ = 'aws_resources'
    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String, index=True)
    arn = Column(String, unique=True, index=True)
    region = Column(String)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "resource_type": self.resource_type,
            "arn": self.arn,
            "region": self.region,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }