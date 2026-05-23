import os
from dotenv import load_dotenv

load_dotenv()  # Load .env in dev

class Config:
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_CLIENT_ID = os.getenv("STRIPE_CLIENT_ID")
    STRIPE_CLIENT_SECRET = os.getenv("STRIPE_CLIENT_SECRET")
    DATA_LAKE_PATH = os.getenv("DATA_LAKE_PATH", "/data/stripe")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")