from dataclasses import dataclass
from datetime import datetime

@dataclass
class SignatureDTO:
    service: str
    version: str
    signature_hash: str          # **decrypted** value
    created_at: datetime