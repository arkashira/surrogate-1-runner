from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Request(Base):
    __tablename__ = "requests"
    
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending")
    # Other fields...
    
    # Relationship to status transitions
    status_transitions = relationship("StatusTransition", back_populates="request")
    timeline_events = relationship("TimelineEvent", back_populates="request")

class StatusTransition(Base):
    __tablename__ = "status_transitions"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"))
    from_status = Column(String)
    to_status = Column(String)
    actor = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship back to request
    request = relationship("Request", back_populates="status_transitions")

class TimelineEvent(Base):
    __tablename__ = "timeline_events"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)
    actor = Column(String)
    # Link to status transition if applicable
    status_transition_id = Column(Integer, ForeignKey("status_transitions.id"))
    
    # Relationships
    request = relationship("Request", back_populates="timeline_events")
    status_transition = relationship("StatusTransition")