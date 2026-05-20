import os
import pyotp
import logging
from typing import Optional

class MultiFactorAuth:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_totp_secret(self) -> str:
        """Generate a TOTP secret for a user."""
        secret = pyotp.random_base32()
        self.logger.info("Generated TOTP secret")
        return secret

    def verify_totp(self, secret: str, token: str) -> bool:
        """Verify a TOTP token."""
        totp = pyotp.TOTP(secret)
        is_valid = totp.verify(token)
        self.logger.info(f"TOTP verification result: {is_valid}")
        return is_valid

    def generate_backup_codes(self, num_codes: int = 5) -> list:
        """Generate backup codes for a user."""
        backup_codes = [pyotp.random_base32() for _ in range(num_codes)]
        self.logger.info(f"Generated {num_codes} backup codes")
        return backup_codes

    def verify_backup_code(self, backup_codes: list, code: str) -> bool:
        """Verify a backup code."""
        is_valid = code in backup_codes
        self.logger.info(f"Backup code verification result: {is_valid}")
        return is_valid