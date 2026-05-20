from typing import List
from .base_model import BaseModelWithHKT

class ExampleModel(BaseModelWithHKT['ExampleModel']):
    items: List[str]

    def add_item(self, item: str) -> 'ExampleModel':
        self.items.append(item)
        return self