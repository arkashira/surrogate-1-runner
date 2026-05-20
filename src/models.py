from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    learned_terms = db.relationship('Term', secondary='user_learned_terms', backref='learners')

class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    example = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)

user_learned_terms = db.Table('user_learned_terms',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('term_id', db.Integer, db.ForeignKey('term.id'), primary_key=True)
)