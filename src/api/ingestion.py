import csv
import io
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import text

# Assuming a database dependency exists in the project structure
# If not, we implement a minimal mock/placeholder for the engine
from src.database import get_db 

router = APIRouter()

def process_aws_csv(file_content: bytes, db_session_factory):
    """
    Background task to process CSV and insert into cost_records.
    Uses ON CONFLICT DO NOTHING to handle duplicates (timestamp + resource_id).
    """
    stream = io.StringIO(file_content.decode("utf-8"))
    reader = csv.DictReader(stream)
    
    # We open a new session for the background task
    session = db_session_factory()
    try:
        for row in reader:
            # Expected CSV columns: timestamp, resource_id, cost, currency, service
            # Example: 2023-10-01T12:00:00Z, i-1234567890abcdef0, 0.05, USD, ec2
            
            query = text("""
                INSERT INTO cost_records (timestamp, resource_id, cost, currency, service)
                VALUES (:ts, :rid, :cost, :curr, :svc)
                ON CONFLICT (timestamp, resource_id) DO NOTHING
            """)
            
            session.execute(query, {
                "ts": row["timestamp"],
                "rid": row["resource_id"],
                "cost": float(row["cost"]),
                "curr": row["currency"],
                "svc": row["service"]
            })
        session.commit()
    except Exception as e:
        session.rollback()
        # In a real system, we would log this to an error tracking service
        print(f"Ingestion error: {e}")
    finally:
        session.close()

@router.post("/ingest/aws", status_code=202)
async def ingest_aws_cost_data(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = None # Provided by dependency injection
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    content = await file.read()
    
    # We pass the session factory or a way to create sessions to the background task
    # because the request-scoped session will be closed when the response is sent.
    from src.database import SessionLocal
    background_tasks.add_task(process_aws_csv, content, SessionLocal)
    
    return {"message": "Ingestion started"}