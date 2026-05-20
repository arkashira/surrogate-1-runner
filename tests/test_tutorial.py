import unittest
from surrogate_1 import Functor, Monad

class TestTutorialExamples(unittest.TestCase):
    def test_simple_functor(self):
        class SimpleFunctor(Functor):
            def __init__(self, value):
                self.value = value

            def map(self, func):
                return SimpleFunctor(func(self.value))

        simple_functor = SimpleFunctor(5)
        transformed_functor = simple_functor.map(lambda x: x * 2)
        self.assertEqual(transformed_functor.value, 10)

    def test_simple_monad(self):
        class SimpleMonad(Monad):
            def __init__(self, value):
                self.value = value

            def bind(self, func):
                return func(self.value)

        simple_monad = SimpleMonad(10)
        result = simple_monad.bind(lambda x: x + 5).bind(lambda x: x * 2)
        self.assertEqual(result, 30)

    def test_combined_functor_monad(self):
        class CombinedFunctorMonad(Functor, Monad):
            def __init__(self, value):
                self.value = value

            def map(self, func):
                return CombinedFunctorMonad(func(self.value))

            def bind(self, func):
                return func(self.value)

        combined = CombinedFunctorMonad(15)
        transformed_combined = combined.map(lambda x: x + 10).bind(lambda x: x * 3)
        self.assertEqual(transformed_combined, 75)

if __name__ == '__main__':
    unittest.main()