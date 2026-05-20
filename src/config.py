from pathlib import Path


class Config:
    """
    Centralised configuration for the surrogate service.
    """

    def __init__(self, service_name: str):
        self.service_name = service_name
        # Base directory can be overridden via env var for easier testing
        base = Path(
            getenv("SCHEMA_STORAGE_ROOT", "/opt/axentx/surrogate-1/storage/schemas")
        )
        self.schema_storage_path = base / service_name

    def __repr__(self) -> str:
        return f"Config(service_name={self.service_name!r}, schema_storage_path={self.schema_storage_path})"