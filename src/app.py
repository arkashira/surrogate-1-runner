import logging
from flask import Flask, request, redirect, session, url_for, jsonify
import stripe
from .config import Config

app = Flask(__name__)
app.secret_key = Config.FLASK_SECRET_KEY

# Configure Stripe
stripe.api_key = Config.STRIPE_SECRET_KEY

# Logging
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

@app.route("/stripe/oauth")
def stripe_oauth():
    """
    1️⃣ If `code` is present → exchange it for an access token.  
    2️⃣ Otherwise → redirect the user to Stripe’s OAuth consent page.
    """
    code = request.args.get("code")
    if code:
        try:
            token_resp = stripe.OAuth.token(
                grant_type="authorization_code",
                code=code,
            )
            session["stripe_access_token"] = token_resp["access_token"]
            return redirect(url_for("stripe_success"))
        except stripe.error.StripeError as exc:
            logger.exception("Stripe OAuth token exchange failed")
            return redirect(url_for("stripe_error", error=str(exc)))
    else:
        try:
            auth_url = stripe.OAuth.authorize_url(
                client_id=Config.STRIPE_CLIENT_ID,
                scope="read_write",
                redirect_uri=url_for("stripe_oauth", _external=True),
            )
            return redirect(auth_url)
        except Exception as exc:
            logger.exception("Failed to build Stripe OAuth URL")
            return redirect(url_for("stripe_error", error=str(exc)))

@app.route("/stripe/success")
def stripe_success():
    return jsonify({"message": "Stripe account connected successfully!"})

@app.route("/stripe/error")
def stripe_error():
    error = request.args.get("error", "Unknown error")
    return jsonify({"error": error}), 400

# Expose the app for tests
__all__ = ["app"]