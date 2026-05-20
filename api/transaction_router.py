from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import TransactionLog
from .transaction_schema import TransactionSchema, TransactionLogBase
from .services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["Transactions"])

transaction_service = TransactionService()

@router.post("/capture/")
async def capture_transaction_logs(logs: List[TransactionLogBase]):
    try:
        captured_logs = await transaction_service.capture_transaction_logs(logs)
        return captured_logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/compare_transaction_logs/")
async def compare_transaction_logs(db: Session = Depends(get_db)):
    mysql_logs = db.query(TransactionLog).filter_by(database_type="mysql").all()
    mariadb_logs = db.query(TransactionLog).filter_by(database_type="mariadb").all()

    comparison_results = []
    for mysql_log in mysql_logs:
        matching_mariadb_log = next((log for log in mariadb_logs if log.transaction_id == mysql_log.transaction_id), None)
        if matching_mariadb_log:
            comparison_results.append({
                "transaction_id": mysql_log.transaction_id,
                "mysql_commit_status": mysql_log.commit_status,
                "mariadb_commit_status": matching_mariadb_log.commit_status,
                "isolation_level_mysql": mysql_log.isolation_level,
                "isolation_level_mariadb": matching_mariadb_log.isolation_level
            })

    return {"comparison_results": comparison_results}