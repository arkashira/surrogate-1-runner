class LLMError(Exception):
    """
    Standardized error wrapper for LLM provider errors.
    Contains error code, message, and originating provider.
    """
    def __init__(self, code: str, message: str, provider: str):
        super().__init__(f"[{provider}] {code}: {message}")
        self.code = code
        self.message = message
        self.provider = provider

    def __repr__(self):
        return f"LLMError(provider='{self.provider}', code='{self.code}', message='{self.message}')"