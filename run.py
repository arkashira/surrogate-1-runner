from flask import Flask
from dashboard.models import db
from dashboard.routes import bp  # Blueprint defined in routes.py

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="replace‑with‑strong‑secret",
        SQLALCHEMY_DATABASE_URI="sqlite:///surrogate1.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    # Register blueprint that holds all UI routes
    app.register_blueprint(bp)

    # Make current year available to every template
    @app.context_processor
    def inject_current_year():
        from datetime import datetime
        return {"current_year": datetime.utcnow().year}

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()          # creates tables on first run
    app.run(host="0.0.0.0", port=5000, debug=True)