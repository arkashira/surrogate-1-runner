
from typing import Callable, Generic, TypeVar

T = TypeVar('T')
U = TypeVar('U')

class Functor(Generic[T, U]):
    """
    A Functor is a type that can be mapped over. It represents a container-like structure that can be transformed without changing its underlying structure.

    Example:
        >>> from src.functor_monad import Functor
        >>> functor = Functor(5)
        >>> mapped_functor = functor.map(lambda x: x * 2)
        >>> print(mapped_functor.value)
        10
    """

    def __init__(self, value: T):
        self.value = value

    def map(self, func: Callable[[T], U]) -> 'Functor[U]':
        """
        Applies a function to the value contained within the Functor.

        Args:
            func (function): A function to apply to the value.

        Returns:
            Functor: A new Functor instance with the transformed value.
        """
        return Functor(func(self.value))

class Monad(Functor[T, U]):
    """
    A Monad is a design pattern that allows for chaining operations in a functional style. It represents a computation that can be sequenced.

    Example:
        >>> from src.functor_monad import Monad
        >>> monad = Monad(5)
        >>> result = monad.bind(lambda x: Monad(x * 2)).bind(lambda x: Monad(x + 3))
        >>> print(result.value)
        13
    """

    def bind(self, func: Callable[[T], Monad[U]]) -> Monad[U]:
        """
        Applies a function to the value contained within the Monad and flattens the result.

        Args:
            func (function): A function to apply to the value.

        Returns:
            Monad: A new Monad instance with the transformed value.
        """
        return func(self.value).map(type(self).__call__).value