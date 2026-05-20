
from fastapi import FastAPI, HTTPException, Query
from typing import List
from pydantic import BaseModel
import json
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Database connection
engine = create_engine('postgresql://user:password@localhost/mydatabase')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class ComponentFilter(BaseModel):
    category: str = None
    price_range: str = None
    brand: str = None
    key_spec: str = None

class Component(BaseModel):
    id: int
    name: str
    price: float
    performance: float
    brand: str
    key_spec: str

@app.get("/components/filtered", response_model=List[Component])
def get_filtered_components(filter: ComponentFilter = Query()):
    session = SessionLocal()

    query = session.query(Component)

    if filter.category:
        query = query.filter(Component.category == filter.category)

    if filter.price_range:
        query = query.filter(Component.price >= float(filter.price_range.split('-')[0]))
        query = query.filter(Component.price <= float(filter.price_range.split('-')[1]))

    if filter.brand:
        query = query.filter(Component.brand == filter.brand)

    if filter.key_spec:
        query = query.filter(Component.key_spec == filter.key_spec)

    result = query.all()

    session.close()

    return result

# src/api/__init__.py

from fastapi import FastAPI
from .components import app as components_app

app = FastAPI()

app.include_router(components_app)