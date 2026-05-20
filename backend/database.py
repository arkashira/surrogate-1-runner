from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initialise the DB and create tables if they do not exist."""
    db.init_app(app)
    with app.app_context():
        db.create_all()