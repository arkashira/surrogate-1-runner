import unittest
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from os import urandom
from hashlib import sha256
from base64 import b64encode, b64decode
from pathlib import Path
from json import dumps, loads

class TestSecurity(unittest.TestCase):

    def setUp(self):
        self.key = urandom(32)
        self.iv = urandom(16)
        self.data = b'This is some sensitive data'
        self.audit_log_path = '/tmp/audit.log'

    def test_aes_encryption(self):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(self.data) + padder.finalize()
        ct = encryptor.update(padded_data) + encryptor.finalize()

        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(ct) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        self.assertEqual(self.data, decrypted_data)

    def test_key_rotation(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'salt',
            iterations=100000,
            backend=default_backend()
        )
        key_1 = kdf.derive(b'password')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'salt',
            iterations=100000,
            backend=default_backend()
        )
        key_2 = kdf.derive(b'new_password')

        self.assertNotEqual(key_1, key_2)

    def test_audit_logging(self):
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'api_key_id': 'test_api_key_id',
            'endpoint': '/v1/sensor/data',
            'response_status': 200
        }
        with open(self.audit_log_path, 'a') as f:
            f.write(dumps(audit_entry) + '\n')

        with open(self.audit_log_path, 'r') as f:
            lines = f.readlines()
            last_entry = loads(lines[-1])

        self.assertEqual(last_entry['api_key_id'], 'test_api_key_id')
        self.assertEqual(last_entry['endpoint'], '/v1/sensor/data')
        self.assertEqual(last_entry['response_status'], 200)

if __name__ == '__main__':
    unittest.main()