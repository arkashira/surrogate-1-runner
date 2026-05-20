import unittest
from unittest.mock import Mock
from axentx.daemon import config
from axentx.daemon import tenant
from stripe_webhook import stripe_webhook

class TestStripeWebhook(unittest.TestCase):
    def setUp(self):
        self.config = config.get()
        self.tenant = tenant.get()

    def test_handle_webhook_checkout_session_completed(self):
        event = {
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'metadata': {
                        'tenant_id': 'test_tenant'
                    },
                    'plan': {
                        'nickname': 'plan'
                    },
                    'line_items': {
                        'data': [
                            {
                                'price': {
                                    'id': 'price_id'
                                }
                            }
                        ]
                    }
                }
            }
        }

        response = stripe_webhook(event)
        self.assertEqual(response, {'status': 'ok'})

    def test_handle_webhook_invalid_event_type(self):
        event = {
            'type': 'invalid_event_type'
        }

        response = stripe_webhook(event)
        self.assertEqual(response, {'status': 'error', 'error': 'Invalid event type'})

if __name__ == '__main__':
    unittest.main()