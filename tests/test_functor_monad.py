
import unittest
from src.functor_monad import Functor, Monad

class TestFunctorMonad(unittest.TestCase):
    def test_functor_map(self):
        functor = Functor(5)
        mapped_functor = functor.map(lambda x: x * 2)
        self.assertEqual(mapped_functor.value, 10)

    def test_monad_bind(self):
        monad = Monad(5)
        result = monad.bind(lambda x: Monad(x * 2)).bind(lambda x: Monad(x + 3))
        self.assertEqual(result.value, 13)

if __name__ == '__main__':
    unittest.main()