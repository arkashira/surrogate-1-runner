"""
Functor utilities for the surrogate-1 project.

This module defines a ``Functor`` protocol that captures the minimal
interface required for a type to be considered a functor: it must
provide a ``fmap`` method that maps a function over its contained value
and returns a new functor instance.

The ``fmap`` function provided here is a convenience wrapper that
dispatches to the ``fmap`` method of any object satisfying the protocol.
"""

from __future__ import annotations

from typing import Callable, Generic, Protocol, TypeVar, runtime_checkable

T = TypeVar("T")
U = TypeVar("U")


@runtime_checkable
class Functor(Protocol[T]):
    """
    Protocol representing a Functor.

    A Functor must implement a ``fmap`` method that takes a callable
    ``func`` and returns a new Functor containing the result of applying
    ``func`` to the original value.
    """

    def fmap(self, func: Callable[[T], U]) -> "Functor[U]":
        """Map ``func`` over the functor's contents."""


def fmap(func: Callable[[T], U], functor: Functor[T]) -> Functor[U]:
    """
    Apply ``func`` to ``functor`` using the functor's ``fmap`` method.

    This is a thin wrapper that enables a uniform functional style:

    >>> from surrogate_1.functor import fmap
    >>> result = fmap(lambda x: x + 1, some_functor)

    Parameters
    ----------
    func:
        A callable that transforms a value of type ``T`` to ``U``.
    functor:
        An instance that conforms to the :class:`Functor` protocol.

    Returns
    -------
    Functor[U]
        A new functor containing the transformed value.
    """
    return functor.fmap(func)