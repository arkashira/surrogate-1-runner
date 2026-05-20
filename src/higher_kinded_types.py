from typing import TypeVar, Generic, Callable, Any

# Define higher-kinded type variables
F = TypeVar('F', bound=type)  # For type constructors
HKT = TypeVar('HKT', bound=Callable[..., Any])  # For value-level operations

class Functor(Generic[F]):
    """Functor type constructor with map operation"""
    def __init__(self, value: F):
        self.value = value

    def map(self, func: Callable[[F], F]) -> 'Functor[F]':
        """Apply a function to the contained value"""
        return Functor(func(self.value))

class Monad(Generic[F]):
    """Monad type constructor with bind operation"""
    def __init__(self, value: F):
        self.value = value

    def bind(self, func: Callable[[F], 'Monad[F]']) -> 'Monad[F]':
        """Sequence computations by passing the result of one to the next"""
        return func(self.value)

    @classmethod
    def unit(cls, value: F) -> 'Monad[F]':
        """Lift a value into the monadic context"""
        return cls(value)

# Example usage
def example_usage():
    # Functor example
    functor = Functor(5)
    doubled_functor = functor.map(lambda x: x * 2)
    print(f"Functor result: {doubled_functor.value}")  # Output: 10

    # Monad example
    monad = Monad.unit(5)
    doubled_monad = monad.bind(lambda x: Monad.unit(x * 2))
    print(f"Monad result: {doubled_monad.value}")  # Output: 10

if __name__ == "__main__":
    example_usage()