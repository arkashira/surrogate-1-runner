from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # other fields...

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # other fields...

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recommendation_id = db.Column(db.Integer, db.ForeignKey('recommendation.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    feedback_text = db.Column(db.Text)
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())