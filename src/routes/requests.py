from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from sqlalchemy import func
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///requests.db')
Base = declarative_base()

class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

router = APIRouter()

@router.patch("/requests/{id}/status", response_model=StatusUpdate)
async def update_status(id: int, status_update: StatusUpdate):
    try:
        request = session.query(Request).filter(Request.id == id).first()
        if request is None:
            raise HTTPException(status_code=404, detail="Request not found")
        previous_status = request.status
        request.status = status_update.status
        request.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(request)
        status_event = StatusEvent(
            request_id=id,
            status=status_update.status,
            previous_status=previous_status,
            timestamp=datetime.now(),
            actor=status_update.actor,
        )
        status_event_repo.save(status_event)
        return status_update
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))