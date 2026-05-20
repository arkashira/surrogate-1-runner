from sqlalchemy.orm import Session
from .models import Alert

def get_alert(db: Session, alert_id: int):
    return db.query(Alert).filter(Alert.id == alert_id).first()

def mute_alert(db: Session, alert: Alert):
    alert.is_muted = True
    db.commit()
    db.refresh(alert)