
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict
from dataclasses import dataclass
import random
import json
from src.data import generate_synthetic_data

app = FastAPI()

class SyntheticData(BaseModel):
    data_format: str
    data: str

@dataclass
class SyntheticDataResponse:
    data_format: str
    data: Dict

@app.get("/synthetic-data", response_model=SyntheticDataResponse)
def get_synthetic_data():
    data_format = random.choice(["json", "csv", "xml"])
    data = generate_synthetic_data(data_format)
    return SyntheticDataResponse(data_format=data_format, data=data)

@app.get("/synthetic-data/{data_format}", response_model=SyntheticData)
def get_synthetic_data_by_format(data_format: str):
    if data_format not in ["json", "csv", "xml"]:
        raise HTTPException(status_code=400, detail="Unsupported data format")
    data = generate_synthetic_data(data_format)
    return SyntheticData(data_format=data_format, data=data)

@app.post("/synthetic-data", response_model=SyntheticData)
def get_synthetic_data_by_request(body: SyntheticData):
    if body.data_format not in ["json", "csv", "xml"]:
        raise HTTPException(status_code=400, detail="Unsupported data format")
    return body