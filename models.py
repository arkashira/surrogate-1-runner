from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Pipeline(Base):
    __tablename__ = 'pipelines'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    statuses = relationship("PipelineStatus", back_populates="pipeline")

class PipelineStatus(Base):
    __tablename__ = 'pipeline_statuses'

    id = Column(Integer, primary_key=True)
    pipeline_id = Column(Integer, ForeignKey('pipelines.id'))
    status = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    pipeline = relationship("Pipeline", back_populates="statuses")