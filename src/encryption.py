"""
AES‑256 encryption helper.

* Uses a 256‑bit key (32 bytes) and a 128‑bit IV.
* Default mode is CFB – it is stream‑cipher‑friendly and does not require padding.
* Provides a static key‑derivation helper (PBKDF2‑HMAC‑SHA256).

The implementation follows the best‑practice guidelines from the
Python Cryptography Authority (PyCA) and the OWASP Crypto Cheat Sheet.
"""

import os
from typing import Optional

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class AES256Encryption:
    """Encrypt / decrypt data with AES‑256 in CFB mode."""

    def __init__(self, key: Optional[bytes] = None) -> None:
        """
        Parameters
        ----------
        key : bytes | None
            32‑byte key.  If omitted, a fresh random key is generated.
        """
        self.backend = default_backend()
        self.key = key or os.urandom(32)

    # ------------------------------------------------------------------ #
    #  Encryption / Decryption
    # ------------------------------------------------------------------ #
    def encrypt(self, data: bytes) -> bytes:
        """Return IV + ciphertext."""
        iv = os.urandom(16)  # 128‑bit IV
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ct = encryptor.update(data) + encryptor.finalize()
        return iv + ct

    def decrypt(self, data: bytes) -> bytes:
        """Accept IV + ciphertext and return plaintext."""
        iv, ct = data[:16], data[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        return decryptor.update(ct) + decryptor.finalize()

    # ------------------------------------------------------------------ #
    #  Key derivation
    # ------------------------------------------------------------------ #
    @staticmethod
    def derive_key(password: str, salt: bytes, iterations: int = 100_000) -> bytes:
        """
        Derive a 256‑bit key from a password.

        Parameters
        ----------
        password : str
            User supplied password.
        salt : bytes
            Random salt (>= 16 bytes recommended).
        iterations : int
            Number of PBKDF2 iterations – 100 000 is a good default.

        Returns
        -------
        bytes
            32‑byte derived key.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
            backend=default_backend(),
        )
        return kdf.derive(password.encode())