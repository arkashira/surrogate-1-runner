import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

import stripe
from fastapi import APIRouter, Request, HTTPException, Header, status
from flask import Flask, request, jsonify

from axentx.daemon import config
from axentx.daemon import tenant

# Configure logging
logger = logging.getLogger("stripe_webhook")
logger.setLevel(logging.INFO)

# Stripe secret keys (test mode)
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
if not STRIPE_WEBHOOK_SECRET:
    raise RuntimeError("STRIPE_WEBHOOK_SECRET environment variable not set")

# Billing data directory
BILLING_DIR = Path(config.get('billing_data_dir'))
BILLING_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()

def _save_billing_record(tenant_id: str, record: Dict[str, Any]) -> None:
    """
    Persist the billing record as a JSON file named after the tenant ID.
    """
    file_path = BILLING_DIR / f"{tenant_id}.json"
    with file_path.open("w", encoding="utf-8") as fp:
        json.dump(record, fp, indent=2, default=str)
    logger.info("Saved billing record for tenant %s", tenant_id)

def _load_billing_record(tenant_id: str) -> Dict[str, Any]:
    """
    Load existing billing record if present, otherwise return an empty dict.
    """
    file_path = BILLING_DIR / f"{tenant_id}.json"
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    return {}

@router.post("/stripe/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(..., alias="Stripe-Signature"),
) -> Dict[str, str]:
    """
    Handle Stripe webhook events.

    Expected events:
      - checkout.session.completed
      - invoice.payment_succeeded

    The tenant ID is extracted from the session metadata.
    """
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=stripe_signature,
            secret=STRIPE_WEBHOOK_SECRET,
        )
    except stripe.error.SignatureVerificationError as e:
        logger.warning("Invalid Stripe signature: %s", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature")
    except Exception as e:
        logger.error("Error parsing Stripe webhook: %s", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    # Process relevant event types
    if event["type"] in ("checkout.session.completed", "invoice.payment_succeeded"):
        data_object = event["data"]["object"]
        # Extract tenant ID from metadata (assumed to be set during checkout)
        tenant_id = data_object.get("metadata", {}).get("tenant_id")
        if not tenant_id:
            logger.warning("Missing tenant_id in event metadata")
            return {"status": "ignored"}

        # Build billing record
        record = _load_billing_record(tenant_id)
        record.update(
            {
                "last_payment_date": datetime.utcnow().isoformat() + "Z",
                "plan": data_object.get("plan", {}).get("nickname", "unknown"),
                "price_id": data_object.get("line_items", {}).get("data", [{}])[0].get("price", {}).get("id"),
                "status": "active",
                "stripe_event_id": event["id"],
            }
        )
        _save_billing_record(tenant_id, record)
        tenant.update_config(tenant_id, record['plan'])
        logger.info("Processed Stripe event %s for tenant %s", event["id"], tenant_id)

    return {"status": "ok"}

# Flask app for handling incoming webhook requests
app = Flask(__name__)

@app.route('/stripe/webhook', methods=['POST'])
def stripe_webhook_flask():
    return jsonify(stripe_webhook(request))

if __name__ == '__main__':
    app.run(debug=True)