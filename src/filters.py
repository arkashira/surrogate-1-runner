
from datetime import timedelta
from typing import Dict, Any

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, and_, or_

app = FastAPI()

# Assuming you have a database model for CostData
# and a table named cost_data
db_url = "postgresql://user:password@localhost/cost_data_db"
engine = create_engine(db_url)

class TimeRangeFilter(BaseModel):
    start_date: str
    end_date: str

class ServiceFilter(BaseModel):
    service: str

@app.get("/cost_data/filter/")
async def get_filtered_cost_data(time_range: TimeRangeFilter, service: ServiceFilter):
    start_date = pd.to_datetime(time_range.start_date)
    end_date = pd.to_datetime(time_range.end_date)

    query = (
        f"SELECT * FROM cost_data WHERE service = '{service.service}' AND timestamp BETWEEN '{start_date}' AND '{end_date}'"
    )

    with engine.connect() as connection:
        result = connection.execute(query).fetchall()

    if not result:
        raise HTTPException(status_code=404, detail="No data found for the given filters")

    return result