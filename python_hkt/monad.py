from typing import TypeVar, Generic, Callable

T = TypeVar('T')
M = TypeVar('M', bound='Monad')

class Monad(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def bind(self: M, func: Callable[[T], M]) -> M:
        return func(self.value)

    def map(self, func: Callable[[T], T]) -> 'Monad[T]':
        return Monad(func(self.value))

    @classmethod
    def unit(cls, value: T) -> 'Monad[T]':
        return cls(value)

# Example usage:
class Maybe(Monad[T]):
    def __init__(self, value: T | None) -> None:
        super().__init__(value)

    @classmethod
    def unit(cls, value: T) -> 'Maybe[T]':
        return cls(value)

    def bind(self, func: Callable[[T], 'Maybe[T]']) -> 'Maybe[T]':
        if self.value is None:
            return Maybe(None)
        else:
            return func(self.value)

# Test cases
def test_monad():
    m = Maybe.unit(5)
    result = m.bind(lambda x: Maybe.unit(x + 1)).map(lambda x: x * 2)
    assert isinstance(result, Maybe)
    assert result.value == 12

    n = Maybe.unit(None)
    result = n.bind(lambda x: Maybe.unit(x + 1))
    assert isinstance(result, Maybe)
    assert result.value is None

test_monad()