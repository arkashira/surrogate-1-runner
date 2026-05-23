import json
import os
import logging
from datetime import datetime, timedelta

import stripe
from .config import Config

# Logging
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

def refresh_stripe_data():
    """
    Pull the last 24 h of balance transactions and persist them as a JSON file.
    """
    access_token = os.getenv("STRIPE_ACCESS_TOKEN") or Config.STRIPE_SECRET_KEY
    if not access_token:
        raise RuntimeError("Stripe access token not configured")

    stripe.api_key = access_token

    end_ts = int(datetime.utcnow().timestamp())
    start_ts = int((datetime.utcnow() - timedelta(days=1)).timestamp())

    try:
        bal_txns = stripe.BalanceTransaction.list(
            created={"gte": start_ts, "lte": end_ts},
            limit=100,
        )
    except stripe.error.StripeError as exc:
        logger.exception("Failed to list balance transactions")
        raise RuntimeError(f"Stripe API error: {exc}") from exc

    data = []
    for txn in bal_txns.auto_paging_iter():
        data.append(
            {
                "id": txn.id,
                "amount": txn.amount,
                "currency": txn.currency,
                "status": txn.status,
                "created": datetime.fromtimestamp(txn.created).isoformat(),
                "description": txn.description,
                "type": txn.type,
            }
        )

    # Persist
    os.makedirs(Config.DATA_LAKE_PATH, exist_ok=True)
    file_name = f"stripe_data_{datetime.utcnow():%Y%m%d}.json"
    file_path = os.path.join(Config.DATA_LAKE_PATH, file_name)

    with open(file_path, "w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=2)

    logger.info(f"Wrote {len(data)} transactions to {file_path}")

if __name__ == "__main__":
    refresh_stripe_data()