from django.db import models
from django.core.validators import MinLengthValidator
from cryptography.fernet import Fernet
import base64
import os

class Session(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    user_id = models.CharField(max_length=255)
    data = models.BinaryField()
    encrypted = models.BooleanField(default=False)
    encryption_key = models.BinaryField(blank=True, null=True)
    security_measures = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def encrypt_data(self):
        if not self.encrypted:
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            encrypted_data = cipher_suite.encrypt(self.data)
            self.data = encrypted_data
            self.encrypted = True
            self.encryption_key = key
            self.save()

    def decrypt_data(self):
        if self.encrypted:
            cipher_suite = Fernet(self.encryption_key)
            decrypted_data = cipher_suite.decrypt(self.data)
            self.data = decrypted_data
            self.encrypted = False
            self.save()

    def enable_security_measures(self, measures):
        self.security_measures.update(measures)
        self.save()

    def enforce_security_measures(self):
        if self.security_measures.get('require_encryption', False) and not self.encrypted:
            raise ValueError("Encryption is required for this session")
        # Add more security measure enforcements as needed