from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Default config
    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///instance/tips.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSONIFY_PRETTYPRINT_REGULAR=True,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api/tips")

    return app