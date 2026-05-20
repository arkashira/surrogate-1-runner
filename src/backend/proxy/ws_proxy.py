import time
from urllib.parse import urlparse
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.exceptions import InvalidSignature

PRIVATE_KEY_PATH = '/path/to/private/key.pem'

class WsProxy:
    def __init__(self):
        with open(PRIVATE_KEY_PATH, 'rb') as key_file:
            self.private_key = load_pem_private_key(key_file.read(), password=None)

    def validate_signed_url(self, url):
        parsed_url = urlparse(url)
        query_params = dict([param.split('=') for param in parsed_url.query.split('&')])
        
        # Extract the signature and the timestamp from the URL
        signature = bytes.fromhex(query_params['signature'])
        timestamp = int(query_params['timestamp'])

        # Check if the URL has expired
        if time.time() - timestamp > 30:
            raise ValueError("URL has expired")

        # Reconstruct the message that was signed (excluding the signature parameter)
        message = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?timestamp={timestamp}"

        try:
            self.private_key.verify(
                signature,
                message.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False

    def handle_connection(self, url):
        if not self.validate_signed_url(url):
            raise ValueError("Invalid or expired URL")
        
        # Spawn a container and exec into the node using the validated URL
        print(f"Spawning container and executing into node using URL: {url}")

# Example usage
if __name__ == "__main__":
    ws_proxy = WsProxy()
    test_url = "http://example.com/node?timestamp=1620000000&signature=abcdef123456"
    ws_proxy.handle_connection(test_url)