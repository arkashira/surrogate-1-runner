from typing import Generic, TypeVar, Callable

T = TypeVar('T')
F = TypeVar('F')

class Functor(Generic[T]):
    def fmap(self, func: Callable[[T], F]) -> 'Functor[F]':
        raise NotImplementedError("fmap must be implemented by subclasses")