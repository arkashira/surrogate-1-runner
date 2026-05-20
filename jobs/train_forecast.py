import os
import logging
import pickle
import datetime as dt
from pathlib import Path

import pandas as pd
import psycopg2 as pg
import numpy as np
import boto3
from prophet import Prophet
from botocore.exceptions import ClientError

# --------------------------------------------------------------------------- #
# Configuration – read from env or defaults
# --------------------------------------------------------------------------- #
DB_DSN = os.getenv(
    "DB_DSN",
    "dbname=axentx_db user=axentx_user host=db_host password=db_password",
)

S3_BUCKET = os.getenv("S3_BUCKET", "axentx-surrogate-1")
S3_KEY = os.getenv("S3_KEY", "model.pkl")
LOCAL_MODEL_PATH = Path("/tmp/model.pkl")  # used when S3 is unavailable

# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def fetch_cost_data() -> pd.DataFrame:
    """Pull the last 90 days of cost data from Postgres."""
    query = """
        SELECT timestamp, cost
        FROM cost_raw
        ORDER BY timestamp DESC
        LIMIT 90
    """
    with pg.connect(DB_DSN) as conn:
        df = pd.read_sql(query, conn)
    log.info("Fetched %d rows of cost data", len(df))
    return df


def prepare_prophet_df(df: pd.DataFrame) -> pd.DataFrame:
    """Prophet expects columns ds (datetime) and y (float)."""
    df = df.copy()
    df["ds"] = pd.to_datetime(df["timestamp"])
    df = df[["ds", "cost"]].rename(columns={"cost": "y"})
    return df


def evaluate_model(model: Prophet, df: pd.DataFrame) -> float:
    """Return MAPE on the last 30 days (hold‑out)."""
    train, test = df[:-30], df[-30:]
    model.fit(train)
    forecast = model.predict(test[["ds"]])
    mape = np.mean(np.abs((test["y"] - forecast["yhat"]) / test["y"])) * 100
    log.info("MAPE on hold‑out: %.2f%%", mape)
    return mape


def store_model(model: Prophet) -> None:
    """Persist the model to S3; fallback to local file."""
    payload = pickle.dumps(model)
    s3 = boto3.client("s3")
    try:
        s3.put_object(Body=payload, Bucket=S3_BUCKET, Key=S3_KEY)
        log.info("Model stored in s3://%s/%s", S3_BUCKET, S3_KEY)
    except ClientError:
        # S3 not available – write locally for dev
        LOCAL_MODEL_PATH.write_bytes(payload)
        log.warning("S3 unavailable – model written to %s", LOCAL_MODEL_PATH)


def load_model() -> Prophet:
    """Load the latest model from S3 or local fallback."""
    s3 = boto3.client("s3")
    try:
        obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
        model = pickle.loads(obj["Body"].read())
        log.info("Loaded model from S3")
    except ClientError:
        if LOCAL_MODEL_PATH.exists():
            model = pickle.loads(LOCAL_MODEL_PATH.read_bytes())
            log.warning("Loaded model from local file %s", LOCAL_MODEL_PATH)
        else:
            raise RuntimeError("No model found in S3 or local path")
    return model


# --------------------------------------------------------------------------- #
# Main training routine
# --------------------------------------------------------------------------- #
def train_and_store() -> None:
    df_raw = fetch_cost_data()
    df = prepare_prophet_df(df_raw)

    model = Prophet()
    mape = evaluate_model(model, df)

    # Only keep the model if MAPE < 10%
    if mape < 10:
        store_model(model)
    else:
        log.warning("MAPE %.2f%% > 10%% – model not stored", mape)


# --------------------------------------------------------------------------- #
# CLI entry‑point (used by cron or schedule)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    train_and_store()