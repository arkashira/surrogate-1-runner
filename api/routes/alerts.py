from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/alerts/")
def read_alerts(db: Session = Depends(get_db), show_noise: bool = False):
    alerts = crud.get_alerts(db, show_noise=show_noise)
    return alerts

@router.post("/alerts/{alert_id}/override_noise")
def override_noise(alert_id: int, db: Session = Depends(get_db)):
    alert = crud.get_alert(db, alert_id=alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    crud.override_noise(db, alert_id=alert_id)
    return {"message": "Noise classification overridden"}

@router.get("/alerts/{alert_id}")
def read_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = crud.get_alert(db, alert_id=alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert