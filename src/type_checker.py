from typing import TypeVar, Generic, Any, Callable, Type

# Define a higher-kinded type variable
HKT = TypeVar('HKT', bound=Callable[..., Any])

class HigherKindedType(Generic[HKT]):
    def __init__(self, type_constructor: Type[HKT]):
        self.type_constructor = type_constructor

    def __call__(self, *args: Any, **kwargs: Any) -> HKT:
        return self.type_constructor(*args, **kwargs)

# Example usage
def functor_example():
    from typing import List, TypeVar

    T = TypeVar('T')

    class Functor(Generic[T]):
        def __init__(self, value: T):
            self.value = value

        def map(self, func: Callable[[T], T]) -> 'Functor[T]':
            return Functor(func(self.value))

    # Define a higher-kinded type variable for Functor
    F = HigherKindedType(Functor)

    # Create a Functor instance
    functor_instance = F(List[int])([1, 2, 3])

    # Use the map method
    mapped_functor = functor_instance.map(lambda x: x * 2)

    print(mapped_functor.value)  # Output: [2, 4, 6]

if __name__ == "__main__":
    functor_example()