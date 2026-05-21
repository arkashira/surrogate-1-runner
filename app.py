from flask import Flask
from dashboard_api import dashboard_api

def create_app():
    app = Flask(__name__)
    app.register_blueprint(dashboard_api)
    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)