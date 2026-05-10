"""
Top‑level package for the surrogate‑1 diagnostic capture service.
"""

from __future__ import annotations

from flask import Flask
from .api.diagnostics import diagnostics_bp
from .database import engine, db_session
from .models.diagnostic import Base

def create_app() -> Flask:
    """Create and configure a Flask application."""
    app = Flask(__name__)

    # Optional: expose the database URL in the config for debugging
    app.config["SQLALCHEMY_DATABASE_URI"] = engine.url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Register the diagnostics blueprint
    app.register_blueprint(diagnostics_bp)

    # Create tables if they don't exist (development / test)
    Base.metadata.create_all(engine)

    return app

# A ready‑to‑run app for `flask run`
app = create_app()