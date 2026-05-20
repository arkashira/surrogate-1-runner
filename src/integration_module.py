"""
Integration utilities for communicating disk geometry reports to external
storage management systems.

The module provides an extensible framework for sending disk geometry data
to various storage management systems. It uses an abstract base class for
different backends and includes a standardized interface for sending data.

Typical usage:

    from src.integration_module import StorageBackend, RESTStorageBackend, send_geometry_data

    # Example REST integration
    rest_backend = RESTStorageBackend(
        endpoint_url="https://storage-api.example.com/v1/disk-geometry",
        auth_token="your-auth-token"
    )

    success = send_geometry_data(geometry_data, rest_backend)
    print(f"Integration test {'successful' if success else 'failed'}")
"""

import abc
import json
import os
import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)

DEFAULT_ENDPOINT_ENV = "STORAGE_MGMT_ENDPOINT"
DEFAULT_TIMEOUT = 10  # seconds

class StorageBackend(abc.ABC):
    """Abstract base class for storage system integrations"""

    @abc.abstractmethod
    def send_geometry_data(self, data: Dict[str, Any]) -> bool:
        """Send disk geometry data to storage system
        Returns True if successful, False otherwise"""
        pass

class RESTStorageBackend(StorageBackend):
    """Integration with REST-based storage management systems"""

    def __init__(self, endpoint_url: str, auth_token: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT):
        self.endpoint_url = endpoint_url
        self.auth_token = auth_token
        self.timeout = timeout
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self.auth_token:
            self.headers['Authorization'] = f'Bearer {auth_token}'

    def send_geometry_data(self, data: Dict[str, Any]) -> bool:
        try:
            response = requests.post(
                self.endpoint_url,
                data=json.dumps(data),
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send geometry data: {str(e)}")
            return False

def send_geometry_data(
    geometry_data: Dict[str, Any],
    backend: StorageBackend
) -> bool:
    """Standardized interface for geometry data integration"""
    return backend.send_geometry_data(geometry_data)

if __name__ == "__main__":
    # Example usage for testing
    test_data = {
        "disk_id": "sda",
        "cylinders": 16383,
        "heads": 16,
        "sectors_per_track": 63,
        "total_sectors": 1606525632,
        "sector_size": 512,
        "model": "ST4000DM000-1F2164",
        "timestamp": "2026-05-04T12:34:56Z"
    }

    # Example REST integration
    rest_backend = RESTStorageBackend(
        endpoint_url="https://storage-api.example.com/v1/disk-geometry",
        auth_token="your-auth-token"
    )

    success = send_geometry_data(test_data, rest_backend)
    print(f"Integration test {'successful' if success else 'failed'}")