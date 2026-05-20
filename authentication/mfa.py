import os
import pyotp
from cryptography.fernet import Fernet

class MFA:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.fernet = Fernet(self.secret_key)

    def generate_totp(self):
        totp = pyotp.TOTP(self.secret_key)
        return totp.now()

    def verify_totp(self, user_input):
        totp = pyotp.TOTP(self.secret_key)
        return totp.verify(user_input)

    def encrypt_session(self, session_data):
        return self.fernet.encrypt(session_data.encode())

    def decrypt_session(self, encrypted_session):
        return self.fernet.decrypt(encrypted_session).decode()

# /opt/axentx/surrogate-1/authentication/config.py
class Config:
    def __init__(self):
        self.secret_key = os.environ.get('SECRET_KEY')
        self.mfa = MFA(self.secret_key)

    def get_secret_key(self):
        return self.secret_key

    def get_mfa(self):
        return self.mfa