import unittest
from src.higher_kinded_types import Functor, Monad

class TestHigherKindedTypes(unittest.TestCase):
    def test_functor(self):
        functor = Functor(5)
        mapped_functor = functor.map(lambda x: x * 2)
        self.assertEqual(mapped_functor.value, 10)

        # Test with string
        str_functor = Functor("hello")
        mapped_str = str_functor.map(lambda s: s.upper())
        self.assertEqual(mapped_str.value, "HELLO")

    def test_monad(self):
        monad = Monad.unit(5)
        bound_monad = monad.bind(lambda x: Monad.unit(x * 2))
        self.assertEqual(bound_monad.value, 10)

        # Test monad chaining
        result = Monad.unit(3).bind(
            lambda x: Monad.unit(x + 1)
        ).bind(
            lambda x: Monad.unit(x * 2)
        )
        self.assertEqual(result.value, 8)

    def test_unit(self):
        self.assertEqual(Monad.unit(42).value, 42)

if __name__ == '__main__':
    unittest.main()