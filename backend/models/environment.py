from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Environment(Base):
    __tablename__ = 'environments'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_ready = Column(Boolean, default=False)

    @classmethod
    def create(cls, data):
        environment = cls(name=data['name'])
        # Save to database
        # session.add(environment)
        # session.commit()
        return environment

    @classmethod
    def get_by_id(cls, environment_id):
        # Fetch from database
        # environment = session.query(cls).filter_by(id=environment_id).first()
        return environment