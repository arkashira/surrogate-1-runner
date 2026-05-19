from fastapi import FastAPI
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

app = FastAPI()
engine = create_engine('sqlite:///cost_data.db')

@app.get("/anomalies")
def get_anomalies():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    query = text("""
        SELECT date, total_spend, is_anomaly
        FROM cost_anomalies
        WHERE date BETWEEN :start_date AND :end_date
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {'start_date': start_date, 'end_date': end_date})
        anomalies = [dict(row) for row in result.fetchall()]

    return {"anomalies": anomalies}