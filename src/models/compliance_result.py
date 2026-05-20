from src.database import db
from datetime import datetime

class ComplianceResult(db.Model):
    __tablename__ = 'compliance_results'

    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.String(36), unique=True, nullable=False)
    app_id = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(20), default='queued')
    results = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get_by_id(cls, scan_id):
        return cls.query.filter_by(scan_id=scan_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()