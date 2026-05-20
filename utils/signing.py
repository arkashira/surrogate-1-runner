"""
Digital signing utilities for audit evidence.
"""

import base64
import hashlib
import hmac
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional


@dataclass
class DocumentSignature:
    signature_id: str
    document_hash: str
    version_id: str
    signed_at: datetime
    signature_bytes: str
    algorithm: str = "HS256"
    metadata: Dict[str, str] = field(default_factory=dict)


class DocumentSigner:
    """
    Handles HMAC‑SHA256 signing of document hashes.
    """

    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or "axentx-compliance-secret-key-2024"

    def sign_document(
        self,
        document_hash: str,
        version_id: str,
        metadata: Optional[Dict[str, str]] = None,
    ) -> DocumentSignature:
        timestamp = datetime.utcnow()
        payload = f"{document_hash}:{version_id}:{timestamp.isoformat()}"
        signature_bytes = hmac.new(
            self.secret_key.encode(), payload.encode(), hashlib.sha256
        ).digest()
        signature_b64 = base64.b64encode(signature_bytes).decode()

        signature_id = f"sig-{version_id}-{timestamp.strftime('%Y%m%d%H%M%S')}"

        return DocumentSignature(
            signature_id=signature_id,
            document_hash=document_hash,
            version_id=version_id,
            signed_at=timestamp,
            signature_bytes=signature_b64,
            metadata=metadata or {},
        )