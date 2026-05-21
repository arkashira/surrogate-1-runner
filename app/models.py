from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from .database import Base

class WorkflowSchedule(Base):
    __tablename__ = "workflow_schedules"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(String, nullable=False)
    workflow_version = Column(Integer, nullable=False)
    cron_expression = Column(String, nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())