"""
Custom exception hierarchy for the surrogate‑1 SDK.
"""

class MissingCredentialError(Exception):
    """
    Raised when a required API credential is not available.

    The exception stores:
        * ``provider`` – the logical name of the provider
          (e.g. ``'claude'``, ``'openai'``, ``'minimax'``).
        * ``source``   – where we tried to fetch the credential
          (``'environment'`` or ``'vault'``).
        * ``credential_name`` – the exact environment variable that
          should be set (derived from ``provider``).

    The error message is intentionally verbose so the user can fix the
    problem immediately.
    """

    def __init__(self, provider: str, source: str = "environment"):
        """
        Parameters
        ----------
        provider : str
            The API provider for which the credential is missing.
        source : str, optional
            The source that was attempted.  Either ``'environment'`` or
            ``'vault'``.  Defaults to ``'environment'``.
        """
        self.provider = provider
        self.source = source
        self.credential_name = f"{provider.upper()}_API_KEY"

        message = (
            f"Missing credential for provider '{provider}'. "
            f"Attempted source: {source}. "
            f"Set the {self.credential_name} environment variable "
            f"or configure VAULT_PATH to fetch from HashiCorp Vault."
        )
        super().__init__(message)

    # ------------------------------------------------------------------
    # Representation helpers
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"MissingCredentialError(provider={self.provider!r}, "
            f"source={self.source!r})"
        )

    def __str__(self) -> str:
        # ``Exception.__str__`` already returns the message we passed to
        # ``super().__init__``.  We keep it for clarity.
        return super().__str__()