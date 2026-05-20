from typing import Generic, TypeVar, Callable
from .types import Functor

T = TypeVar('T')
F = TypeVar('F')

class ListFunctor(Functor[T], Generic[T]):
    def __init__(self, values: list[T]):
        self.values = values

    def fmap(self, func: Callable[[T], F]) -> 'ListFunctor[F]':
        return ListFunctor([func(value) for value in self.values])