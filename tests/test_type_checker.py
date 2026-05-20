import unittest
from typing import List, Callable, Any
from src.type_checker import HigherKindedType

class TestHigherKindedType(unittest.TestCase):
    def test_higher_kinded_type(self):
        class Functor:
            def __init__(self, value: Any):
                self.value = value

            def map(self, func: Callable[[Any], Any]) -> 'Functor':
                return Functor(func(self.value))

        F = HigherKindedType(Functor)
        functor_instance = F(List[int])([1, 2, 3])
        mapped_functor = functor_instance.map(lambda x: x * 2)

        self.assertEqual(mapped_functor.value, [2, 4, 6])

if __name__ == "__main__":
    unittest.main()