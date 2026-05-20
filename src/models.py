from . import db
import datetime

class ComplianceAudit(db.Model):
    """Represents a compliance audit with status tracking."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, complete, failed
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    config_filename = db.Column(db.String(255), nullable=True)
    documentation = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Audit {self.name}>'