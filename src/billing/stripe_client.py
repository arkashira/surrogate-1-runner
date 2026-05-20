import os
import stripe
from typing import Dict, Any, Tuple
from datetime import timedelta
import time

# Initialize Stripe with environment variables
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY


class StripeClient:
    """Stripe client for handling subscription payments"""
    
    def __init__(self):
        self.client_id = STRIPE_SECRET_KEY
        self.client_secret = STRIPE_PUBLIC_KEY
    
    @classmethod
    def get_client(cls) -> 'StripeClient':
        """Factory method to get configured Stripe client"""
        if not STRIPE_SECRET_KEY:
            raise ValueError("STRIPE_SECRET_KEY environment variable not set")
        return cls()
    
    def create_checkout_session(self, customer_email: str, price_id: str = "price_annual_4800") -> Dict[str, Any]:
        """Create Stripe checkout session with 14-day trial for annual subscription"""
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price": price_id,
                    "quantity": 1,
                }],
                mode="subscription",
                success_url=os.environ.get("STRIPE_SUCCESS_URL", "https://example.com/success"),
                cancel_url=os.environ.get("STRIPE_CANCEL_URL", "https://example.com/cancel"),
                customer_email=customer_email,
                trial_period_days=14,
            )
            return {
                "session_id": session.id,
                "checkout_url": session.url,
                "trial_end": int(time.time() + timedelta(days=14).total_seconds())
            }
        except stripe.error.StripeError as e:
            raise RuntimeError(f"Stripe checkout failed: {str(e)}") from e


def get_stripe_credentials() -> Tuple[str, str]:
    """Retrieve Stripe API credentials"""
    client = StripeClient.get_client()
    return client.client_id, client.client_secret