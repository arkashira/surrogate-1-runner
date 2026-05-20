from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from ...models import Alert
from ...schemas import AlertMute
from ...crud import get_alert, mute_alert

router = APIRouter()

@router.post("/mute", response_model=AlertMute)
def mute_alert_endpoint(alert_id: int, db: Session = Depends(get_db)):
    alert = get_alert(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    mute_alert(db, alert)
    return alert