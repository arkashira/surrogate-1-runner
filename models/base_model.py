from typing import TypeVar, Generic, List, Dict, Any
from pydantic import BaseModel

T = TypeVar('T')

class BaseModelWithHKT(BaseModel, Generic[T]):
    def __init__(self, **data):
        super().__init__(**data)

    @classmethod
    def parse_obj(cls, obj: T) -> 'BaseModelWithHKT':
        return super().parse_obj(obj)

    @classmethod
    def parse_raw(cls, b: bytes, **kwargs: Any) -> 'BaseModelWithHKT':
        return super().parse_raw(b, **kwargs)

    def dict(self, **kwargs: Any) -> Dict[str, Any]:
        return super().dict(**kwargs)

    def json(self, **kwargs: Any) -> str:
        return super().json(**kwargs)