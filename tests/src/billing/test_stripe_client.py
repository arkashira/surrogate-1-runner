import os
import time
import unittest
from unittest.mock import patch, MagicMock
from src.billing.stripe_client import StripeClient, get_stripe_credentials


class TestStripeClient(unittest.TestCase):
    """Test suite for Stripe client configuration"""
    
    def setUp(self):
        # Reset module-level variables before each test
        import src.billing.stripe_client as module
        module.STRIPE_SECRET_KEY = None
        module.STRIPE_PUBLIC_KEY = None
    
    @patch.dict(os.environ, {
        'STRIPE_SECRET_KEY': 'sk_test_mock',
        'STRIPE_PUBLIC_KEY': 'pk_test_mock',
        'STRIPE_SUCCESS_URL': 'https://example.com/success',
        'STRIPE_CANCEL_URL': 'https://example.com/cancel'
    })
    def test_get_client_returns_credentials(self):
        """Test that get_client returns correct credentials"""
        # Need to reimport to pick up patched environment
        import importlib
        import src.billing.stripe_client as module
        importlib.reload(module)
        
        client = module.StripeClient.get_client()
        self.assertEqual(client.client_id, 'sk_test_mock')
        self.assertEqual(client.client_secret, 'pk_test_mock')
    
    @patch.dict(os.environ, {
        'STRIPE_SECRET_KEY': 'sk_test_mock',
        'STRIPE_PUBLIC_KEY': 'pk_test_mock',
        'STRIPE_SUCCESS_URL': 'https://example.com/success',
        'STRIPE_CANCEL_URL': 'https://example.com/cancel'
    })
    @patch('src.billing.stripe_client.stripe.checkout.Session.create')
    def test_create_checkout_session(self, mock_create):
        """Test checkout session creation with trial period"""
        import importlib
        import src.billing.stripe_client as module
        importlib.reload(module)
        
        mock_session = MagicMock()
        mock_session.id = 'cs_test_123'
        mock_session.url = 'https://checkout.stripe.com/test'
        mock_create.return_value = mock_session
        
        client = module.StripeClient.get_client()
        result = client.create_checkout_session('test@example.com')
        
        self.assertEqual(result['session_id'], 'cs_test_123')
        self.assertIn('checkout_url', result)
        self.assertIn('trial_end', result)
        mock_create.assert_called_once()
        
        # Verify trial_period_days was passed
        call_args = mock_create.call_args
        self.assertEqual(call_args.kwargs['trial_period_days'], 14)
    
    @patch.dict(os.environ, {'STRIPE_SECRET_KEY': '', 'STRIPE_PUBLIC_KEY': ''})
    def test_missing_credentials_raises_error(self):
        """Test that missing credentials raise appropriate error"""
        import importlib
        import src.billing.stripe_client as module
        importlib.reload(module)
        
        with self.assertRaises(ValueError) as context:
            module.StripeClient.get_client()
        
        self.assertIn('STRIPE_SECRET_KEY', str(context.exception))


if __name__ == '__main__':
    unittest.main()