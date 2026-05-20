import os
from cryptography.fernet import Fernet

class FileEncryptor:
    def __init__(self, key=None):
        self.key = key if key else Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as file:
            file_data = file.read()
        encrypted_data = self.cipher_suite.encrypt(file_data)
        with open(file_path + '.enc', 'wb') as file:
            file.write(encrypted_data)
        os.remove(file_path)

    def decrypt_file(self, file_path):
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
        with open(file_path.replace('.enc', ''), 'wb') as file:
            file.write(decrypted_data)
        os.remove(file_path)

def main():
    encryptor = FileEncryptor()
    encryptor.encrypt_file('/path/to/markdown/file.md')
    # For decryption, call decrypt_file with the encrypted file path

if __name__ == "__main__":
    main()