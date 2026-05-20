"""
Tests for the Functor implementation.

The tests define a simple ``Box`` type that satisfies the ``Functor``
protocol and verify that the ``fmap`` helper correctly maps functions
over ``Box`` instances.
"""

from __future__ import annotations

from typing import Callable, Generic, TypeVar

import pytest

from surrogate_1.functor import Functor, fmap

T = TypeVar("T")
U = TypeVar("U")


class Box(Generic[T]):
    """
    Minimal concrete Functor implementation used for testing.

    It stores a single value and implements ``fmap`` by applying the
    provided function to that value and wrapping the result in a new
    ``Box``.
    """

    def __init__(self, value: T):
        self.value = value

    def fmap(self, func: Callable[[T], U]) -> "Box[U]":
        return Box(func(self.value))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Box) and self.value == other.value

    def __repr__(self) -> str:
        return f"Box({self.value!r})"


def test_fmap_simple():
    """Mapping a simple function over a Box should produce the expected result."""
    b = Box(2)
    result = fmap(lambda x: x * 3, b)
    assert result == Box(6)


def test_fmap_identity():
    """Mapping the identity function should return an equivalent Box."""
    b = Box("hello")
    result = fmap(lambda x: x, b)
    assert result == b


def test_fmap_type_checking():
    """
    Ensure that objects not implementing the Functor protocol raise a
    ``AttributeError`` when passed to ``fmap``. This mirrors the runtime
    behaviour expected when static type checking is not enforced.
    """
    class NotAFunctor:
        pass

    with pytest.raises(AttributeError):
        fmap(lambda x: x, NotAFunctor())  # type: ignore[arg-type]