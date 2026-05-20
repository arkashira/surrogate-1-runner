class SurrogateError(Exception):
    """
    Raised when the Surrogate service returns a non‑successful response.

    Attributes
    ----------
    message: str
        Human‑readable description of the error.
    payload: dict | None
        The JSON body returned by the server (if any).  May be ``None`` when the
        response could not be decoded as JSON.
    status_code: int | None
        HTTP status code returned by the server.
    """

    def __init__(
        self,
        message: str,
        *,
        payload: dict | None = None,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.payload = payload
        self.status_code = status_code

    def __repr__(self) -> str:  # pragma: no cover – helpful for debugging
        return (
            f"{self.__class__.__name__}(message={self.args[0]!r}, "
            f"status_code={self.status_code!r}, payload={self.payload!r})"
        )