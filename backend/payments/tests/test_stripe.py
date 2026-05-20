from django.test import TestCase
from unittest.mock import patch
from .stripe import create_checkout_session, cancel_subscription, handle_webhook

class StripeIntegrationTest(TestCase):

    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session(self, mock_create):
        mock_create.return_value = {'url': 'test_url'}
        url = create_checkout_session()
        self.assertEqual(url, 'test_url')

    @patch('stripe.Subscription.retrieve')
    @patch('stripe.Subscription.save')
    def test_cancel_subscription(self, mock_save, mock_retrieve):
        mock_retrieve.return_value = {'cancel_at_period_end': False}
        result = cancel_subscription('test_subscription_id')
        self.assertTrue(result)

    @patch('stripe.Webhook.construct_event')
    @patch('stripe.Customer.retrieve')
    @patch('stripe.Subscription.retrieve')
    def test_handle_webhook_checkout_completed(self, mock_subscription, mock_customer, mock_construct_event):
        mock_construct_event.return_value = {'type': 'checkout.session.completed', 'data': {'object': {'customer': 'test_customer_id', 'subscription': 'test_subscription_id'}}}
        mock_customer.return_value = {'metadata': {'user_id': 1}}
        mock_subscription.return_value = {'id': 'test_subscription_id', 'status': 'active'}
        handle_webhook('test_payload', 'test_signature')

    @patch('stripe.Webhook.construct_event')
    def test_handle_webhook_invoice_payment_succeeded(self, mock_construct_event):
        mock_construct_event.return_value = {'type': 'invoice.payment_succeeded', 'data': {'object': {'id': 'test_subscription_id', 'status': 'paid'}}}
        handle_webhook('test_payload', 'test_signature')

    @patch('stripe.Webhook.construct_event')
    def test_handle_webhook_customer_subscription_deleted(self, mock_construct_event):
        mock_construct_event.return_value = {'type': 'customer.subscription.deleted', 'data': {'object': {'id': 'test_subscription_id'}}}
        handle_webhook('test_payload', 'test_signature')