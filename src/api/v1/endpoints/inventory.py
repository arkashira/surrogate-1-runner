from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import json
import time
from .database import get_db

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

class InventoryResponse(BaseModel):
    resources: List[Dict[str, Any]]
    last_updated: str
    total_resources: int

router = APIRouter()

@router.get("/inventory", response_model=InventoryResponse)
async def get_inventory(db_session: get_db):
    """
    Endpoint to retrieve the latest AWS inventory.
    Returns all AWS resources (EC2, S3, IAM, RDS, Lambda) from the database.
    """
    try:
        # Query all AWS resources from the database
        resources = db_session.query(AWSResource).all()
        
        # Format the response
        formatted_resources = []
        for resource in resources:
            formatted_resources.append({
                "resource_type": resource.resource_type,
                "arn": resource.arn,
                "region": resource.region,
                "tags": resource.tags,
                "created_at": resource.created_at.isoformat(),
                "updated_at": resource.updated_at.isoformat()
            })
            
        return InventoryResponse(
            resources=formatted_resources,
            last_updated=datetime.utcnow().isoformat(),
            total_resources=len(formatted_resources)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching inventory: {str(e)}")