"""
Low-latency communication protocol configuration for surrogate-1.
Optimized for <10ms latency, 100+ concurrent connections, and TLS encryption.
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


@dataclass
class ProtocolConfig:
    """
    Configuration for the low-latency communication protocol.
    
    Performance targets:
    - Latency: <10ms end-to-end
    - Throughput: 100+ concurrent connections
    - Security: TLS 1.3 encryption
    """
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8443  # HTTPS port
    max_connections: int = 150
    connection_timeout: float = 30.0
    read_timeout: float = 10.0
    write_timeout: float = 10.0
    
    # Protocol settings for low latency
    message_buffer_size: int = 65536  # 64KB buffer
    chunk_size: int = 8192  # 8KB chunks for streaming
    max_message_size: int = 10 * 1024 * 1024  # 10MB max message
    
    # TLS/SSL encryption settings
    ssl_context: Optional[object] = field(default=None, repr=False)
    ssl_cert_path: str = "/etc/ssl/certs/axentx.crt"
    ssl_key_path: str = "/etc/ssl/private/axentx.key"
    ssl_min_version: str = "TLSv1.3"
    ssl_ciphers: str = "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256"
    
    # Message framing (binary protocol for speed)
    frame_header_size: int = 4  # 4-byte length prefix
    frame_magic: bytes = b"AXNT"  # Magic bytes for frame identification
    
    # Connection pooling
    pool_size: int = 50
    pool_max_overflow: int = 100
    pool_recycle: int = 3600
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Metrics
    metrics_enabled: bool = True
    metrics_port: int = 9090
    metrics_path: str = "/metrics"
    
    @classmethod
    def from_env(cls) -> "ProtocolConfig":
        """Load configuration from environment variables."""
        config = cls()
        
        if os.getenv("AXENTX_HOST"):
            config.host = os.getenv("AXENTX_HOST")
        if os.getenv("AXENTX_PORT"):
            config.port = int(os.getenv("AXENTX_PORT"))
        if os.getenv("AXENTX_MAX_CONNECTIONS"):
            config.max_connections = int(os.getenv("AXENTX_MAX_CONNECTIONS"))
        if os.getenv("AXENTX_SSL_CERT_PATH"):
            config.ssl_cert_path = os.getenv("AXENTX_SSL_CERT_PATH")
        if os.getenv("AXENTX_SSL_KEY_PATH"):
            config.ssl_key_path = os.getenv("AXENTX_SSL_KEY_PATH")
        if os.getenv("AXENTX_MESSAGE_BUFFER_SIZE"):
            config.message_buffer_size = int(os.getenv("AXENTX_MESSAGE_BUFFER_SIZE"))
        
        return config
    
    def validate(self) -> list[str]:
        """Validate configuration and return list of errors."""
        errors = []
        
        if self.port < 1 or self.port > 65535:
            errors.append(f"Invalid port: {self.port}")
        
        if self.max_connections < 100:
            errors.append(f"max_connections must be >= 100, got {self.max_connections}")
        
        if self.read_timeout <= 0:
            errors.append("read_timeout must be positive")
        
        if self.ssl_min_version not in ["TLSv1.2", "TLSv1.3"]:
            errors.append(f"Unsupported SSL version: {self.ssl_min_version}")
        
        return errors


# Global configuration instance
config = ProtocolConfig.from_env()