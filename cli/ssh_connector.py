import os
import ssl
import socket
import time
import requests

class SSHConnector:
    def __init__(self, api_key, target_host, port=22, timeout=2):
        self.api_key = api_key
        self.target_host = target_host
        self.port = port
        self.timeout = timeout
        self.ssl_context = self.create_ssl_context()

    def create_ssl_context(self):
        # Create SSL context with strong security settings
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_cert_chain(certfile='path/to/client_cert.pem', keyfile='path/to/client_key.pem')
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations('path/to/ca_cert.pem')
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Only TLS 1.2 and above
        context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3  # Disable SSLv2 and SSLv3
        return context

    def authenticate(self):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f'https://{self.target_host}/api/auth', headers=headers, verify='path/to/ca_cert.pem')
        if response.status_code != 200:
            raise Exception(f"Authentication failed: {response.text}")

    def connect(self):
        self.authenticate()
        start_time = time.time()
        try:
            with socket.create_connection((self.target_host, self.port), timeout=self.timeout) as sock:
                with self.ssl_context.wrap_socket(sock, server_hostname=self.target_host) as ssock:
                    print(f"Secure connection established to {self.target_host} in {time.time() - start_time:.2f} seconds")
                    return ssock  # Return the secure socket for further interaction
        except Exception as e:
            raise Exception(f"Connection failed: {str(e)}")

if __name__ == "__main__":
    api_key = os.getenv("SURROGATE_API_KEY")
    target_host = os.getenv("TARGET_HOST")
    connector = SSHConnector(api_key, target_host)
    connector.connect()