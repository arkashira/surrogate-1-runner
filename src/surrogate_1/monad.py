from .types import T, R
from abc import ABC, abstractmethod
from typing import Generic, Callable

class Monad(ABC, Generic[T]):
    @abstractmethod
    def bind(self, func: Callable[[T], 'Monad[R]']) -> 'Monad[R]':
        """Chain monadic operations with type safety"""
        pass

    @classmethod
    def return_value(cls, value: T) -> 'Monad[T]':
        """Wrap value in monadic context"""
        instance = cls()
        instance.value = value
        return instance

    def __rshift__(self, func: Callable[[T], 'Monad[R]']) -> 'Monad[R]':
        """Operator syntax for bind (>>=)"""
        return self.bind(func)