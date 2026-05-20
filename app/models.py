from . import db
from datetime import datetime

class Tip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TipFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tip_id = db.Column(db.Integer, db.ForeignKey("tip.id"), nullable=False)
    user_id = db.Column(db.String(80), nullable=False)
    feedback = db.Column(db.String(20), nullable=False)  # 'helpful' | 'irrelevant'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tip = db.relationship("Tip", backref=db.backref("feedback", lazy=True))