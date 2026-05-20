
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
import os

app = FastAPI()

DB_FILE = os.path.join(os.path.dirname(__file__), "analytics.db")

class AnalyticsResponse(BaseModel):
    session_duration: float
    session_frequency: int
    provider_usage: List[str]

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY, start_time TEXT, end_time TEXT, provider TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.get("/analytics")
def get_analytics():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT AVG(jiffies(end_time, start_time)) as session_duration, COUNT(*) as session_frequency, GROUP_CONCAT(provider) as provider_usage FROM (SELECT jiffies(end_time, start_time) as jiffies, start_time, end_time, provider FROM sessions) GROUP BY provider")
    result = c.fetchone()

    if result:
        return AnalyticsResponse(session_duration=result[0], session_frequency=result[1], provider_usage=[result[2].replace(" ", ",")])
    else:
        raise HTTPException(status_code=404, detail="No session data found")

    conn.close()