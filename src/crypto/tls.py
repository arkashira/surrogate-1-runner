import ssl
import json
from typing import Optional

class TLSSSH:
    def __init__(self, config_path: str = '/opt/axentx/surrogate-1/src/config/tls_config.json'):
        self.config = self._load_config(config_path)
        self.context = self._create_ssl_context()

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r') as f:
            return json.load(f)

    def _create_ssl_context(self) -> ssl.SSLContext:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(
            certfile=self.config['certfile'],
            keyfile=self.config['keyfile']
        )
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile=self.config['cafile'])
        return context

    def get_ssl_context(self) -> ssl.SSLContext:
        return self.context