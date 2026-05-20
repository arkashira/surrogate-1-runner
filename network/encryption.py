import ssl
import socket
from cryptography.fernet import Fernet

class Encryption:
    def __init__(self, key):
        self.key = key
        self.cipher_suite = Fernet(key)

    def encrypt(self, data):
        return self.cipher_suite.encrypt(data.encode())

    def decrypt(self, encrypted_data):
        return self.cipher_suite.decrypt(encrypted_data).decode()

def generate_key():
    return Fernet.generate_key()

def create_ssl_context(key, cert):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=cert)
    context.load_verify_locations(cafile=key)
    context.verify_mode = ssl.CERT_REQUIRED
    return context

def secure_shell_session(key, cert):
    encryption = Encryption(key)
    context = create_ssl_context(key, cert)
    server_socket = socket.socket(socket.AF_INET)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)
    print('Server listening on port 8080')
    while True:
        client_socket, address = server_socket.accept()
        ssl_socket = context.wrap_socket(client_socket, server_side=True)
        print('Connection established with', address)
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            decrypted_data = encryption.decrypt(data)
            print('Received:', decrypted_data)
            response = 'Hello, client!'
            encrypted_response = encryption.encrypt(response)
            ssl_socket.send(encrypted_response)
        ssl_socket.close()