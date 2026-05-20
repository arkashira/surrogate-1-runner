from django.test import TestCase
from .models import Session
from cryptography.fernet import Fernet
import base64

class SessionModelTest(TestCase):
    def setUp(self):
        self.session = Session.objects.create(
            session_id='test_session',
            user_id='test_user',
            data=b'test_data'
        )

    def test_encrypt_data(self):
        self.session.encrypt_data()
        self.assertTrue(self.session.encrypted)
        self.assertIsNotNone(self.session.encryption_key)

    def test_decrypt_data(self):
        self.session.encrypt_data()
        self.session.decrypt_data()
        self.assertFalse(self.session.encrypted)

    def test_enable_security_measures(self):
        measures = {'require_encryption': True}
        self.session.enable_security_measures(measures)
        self.assertEqual(self.session.security_measures, measures)

    def test_enforce_security_measures(self):
        measures = {'require_encryption': True}
        self.session.enable_security_measures(measures)
        with self.assertRaises(ValueError):
            self.session.enforce_security_measures()