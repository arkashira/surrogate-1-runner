import stripe
from django.conf import settings
from .models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Monthly Subscription',
                    },
                    'unit_amount': 3000,
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=settings.SUCCESS_URL,
            cancel_url=settings.CANCEL_URL,
        )
        return checkout_session.url
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return None

def cancel_subscription(subscription_id):
    try:
        subscription = stripe.Subscription.retrieve(subscription_id)
        subscription.cancel_at_period_end = True
        subscription.save()
        Subscription.objects.filter(stripe_id=subscription_id).update(status='inactive')
        return True
    except Exception as e:
        print(f"Error canceling subscription: {e}")
        return False

def update_subscription_status(event):
    data = event['data']['object']
    subscription_id = data['id']
    status = data['status']
    Subscription.objects.filter(stripe_id=subscription_id).update(status=status)

def handle_webhook(event):
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer = stripe.Customer.retrieve(session['customer'])
        subscription = stripe.Subscription.retrieve(session['subscription'])
        Subscription.objects.create(
            user_id=customer['metadata']['user_id'],
            stripe_id=subscription['id'],
            status=subscription['status']
        )
    elif event['type'] == 'invoice.payment_succeeded':
        update_subscription_status(event)
    elif event['type'] == 'customer.subscription.deleted':
        cancel_subscription(event['data']['object']['id'])