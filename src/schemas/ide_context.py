from pydantic import BaseModel, Field, ValidationError
from typing import Optional

class IDEContext(BaseModel):
    file_path: str = Field(..., description="The absolute path to the file.")
    content: str = Field(..., description="The content of the file.")
    cursor_position: int = Field(..., ge=0, description="The current cursor position in the file.")
    selection: Optional[str] = Field(None, description="The selected text in the file.")

    @classmethod
    def validate_payload(cls, payload: dict):
        try:
            return cls(**payload)
        except ValidationError as e:
            raise ValueError(f"Invalid payload: {e}")

# Example usage:
# payload = {
#     "file_path": "/path/to/file.py",
#     "content": "def example():\n    pass",
#     "cursor_position": 10,
#     "selection": "example()"
# }
# ide_context = IDEContext.validate_payload(payload)