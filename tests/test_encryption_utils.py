import unittest
from src.encryption_utils import AES256Encryptor

class TestAES256Encryptor(unittest.TestCase):
    def setUp(self):
        self.passcode = "test_passcode"
        self.encryptor = AES256Encryptor(self.passcode)
        self.test_data = "This is a test string for encryption."

    def test_encrypt_decrypt(self):
        encrypted_data = self.encryptor.encrypt(self.test_data)
        decrypted_data = self.encryptor.decrypt(encrypted_data)
        self.assertEqual(self.test_data, decrypted_data)

    def test_wrong_passcode(self):
        wrong_encryptor = AES256Encryptor("wrong_passcode")
        encrypted_data = self.encryptor.encrypt(self.test_data)
        with self.assertRaises(Exception):
            wrong_encryptor.decrypt(encrypted_data)