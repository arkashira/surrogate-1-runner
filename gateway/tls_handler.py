import ssl
import socket
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class TLSHandler:
    """Handles TLS 1.3 secure connections with mutual certificate authentication."""
    
    def __init__(self, cert_file: str, key_file: str, ca_file: str):
        """
        Initialize TLS handler with certificate files.
        
        Args:
            cert_file: Path to client certificate file
            key_file: Path to client private key file
            ca_file: Path to CA certificate file
        """
        self.cert_file = cert_file
        self.key_file = key_file
        self.ca_file = ca_file
        
    def create_secure_connection(self, host: str, port: int, 
                              timeout: float = 2.0) -> Optional[ssl.SSLSocket]:
        """
        Create a TLS 1.3 secure connection to target host.
        
        Args:
            host: Target hostname or IP address
            port: Target port number
            timeout: Connection timeout in seconds
            
        Returns:
            Secure SSL socket or None if connection fails
        """
        try:
            # Create base socket
            sock = socket.create_connection((host, port), timeout=timeout)
            
            # Configure TLS context for TLS 1.3 with mutual auth
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
            context.load_verify_locations(cafile=self.ca_file)
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            
            # Enforce TLS 1.3 only
            context.minimum_version = ssl.TLSVersion.TLSv1_3
            context.maximum_version = ssl.TLSVersion.TLSv1_3
            
            # Perform TLS handshake
            secure_sock = context.wrap_socket(sock, server_hostname=host)
            
            logger.info(f"Secure TLS 1.3 connection established to {host}:{port}")
            return secure_sock
            
        except Exception as e:
            logger.error(f"Failed to establish secure connection to {host}:{port}: {e}")
            return None
    
    def validate_certificate(self, sock: ssl.SSLSocket) -> bool:
        """
        Validate the peer certificate.
        
        Args:
            sock: Active SSL socket
            
        Returns:
            True if certificate is valid, False otherwise
        """
        try:
            cert = sock.getpeercert()
            if not cert:
                logger.warning("No peer certificate received")
                return False
                
            # Basic certificate validation
            logger.debug(f"Peer certificate subject: {cert.get('subject')}")
            logger.debug(f"Peer certificate issuer: {cert.get('issuer')}")
            logger.debug(f"Peer certificate serial: {cert.get('serialNumber')}")
            
            return True
            
        except Exception as e:
            logger.error(f"Certificate validation failed: {e}")
            return False