import ssl

def create_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='/path/to/certificate.pem', keyfile='/path/to/private_key.pem')
    return context

# /opt/axentx/surrogate-1/src/terminal_environment.py
import os
import socketserver
import ssl
from http.server import SimpleHTTPRequestHandler

from ssl_config import create_ssl_context

class SecureTerminalHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
        super().end_headers()

def start_server():
    with socketserver.TCPServer(('localhost', 8000), SecureTerminalHandler) as server:
        server.socket = ssl.wrap_socket(server.socket, server_side=True, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_TLS, certfile='/path/to/certificate.pem', keyfile='/path/to/private_key.pem')
        server.serve_forever()

if __name__ == '__main__':
    start_server()