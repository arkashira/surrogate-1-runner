from typing import TypeVar, Callable, Generic

T = TypeVar('T')
R = TypeVar('R')

class Functor(Generic[T]):
    def fmap(self, func: Callable[[T], R]) -> 'Functor[R]':
        raise NotImplementedError("fmap must be implemented by subclasses")

class ListFunctor(Functor[T]):
    def __init__(self, items: list[T]):
        self.items = items

    def fmap(self, func: Callable[[T], R]) -> 'ListFunctor[R]':
        return ListFunctor([func(item) for item in self.items])

# Example usage
if __name__ == "__main__":
    lf = ListFunctor([1, 2, 3])
    print(lf.fmap(lambda x: x * 2).items)  # Output: [2, 4, 6]