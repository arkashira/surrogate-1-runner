# Stub – replace with your real KMS client (AWS KMS, HashiCorp Vault, etc.)
def get_data_key(key_id: str = None) -> bytes:
    """
    Return a 32‑byte base64‑url‑safe key for Fernet.
    In production this should fetch the key from a KMS and cache it securely.
    """
    import base64, os
    # For demo purposes we generate a static key; DO NOT ship this.
    static_key = os.getenv("STATIC_FERNET_KEY")
    if static_key:
        return base64.urlsafe_b64decode(static_key)
    raise RuntimeError("Encryption key not configured")