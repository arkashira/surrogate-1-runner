from sqlalchemy.orm import Session
from . import models, schemas

def get_alerts(db: Session, show_noise: bool = False):
    if show_noise:
        return db.query(models.Alert).all()
    return db.query(models.Alert).filter(models.Alert.is_noise == False).all()

def get_alert(db: Session, alert_id: int):
    return db.query(models.Alert).filter(models.Alert.id == alert_id).first()

def override_noise(db: Session, alert_id: int):
    alert = get_alert(db, alert_id)
    alert.is_noise = not alert.is_noise
    db.commit()
    db.refresh(alert)
    return alert

def classify_noise_alerts(db: Session):
    # Logic to classify alerts as noise based on historical patterns
    # For example, alerts firing >10x in 24h with no incident created
    # This is a simplified example and actual logic may vary
    alerts = db.query(models.Alert).all()
    for alert in alerts:
        # Assuming there's a related table for incidents and alert firings
        # and the actual logic is more complex
        if alert_firing_count(db, alert.id) > 10 and not incident_created(db, alert.id):
            alert.is_noise = True
            db.commit()
            db.refresh(alert)

def alert_firing_count(db: Session, alert_id: int):
    # Placeholder function to count alert firings in the last 24h
    # Actual implementation depends on the schema of alert firings
    return 0

def incident_created(db: Session, alert_id: int):
    # Placeholder function to check if an incident was created for the alert
    # Actual implementation depends on the schema of incidents
    return False