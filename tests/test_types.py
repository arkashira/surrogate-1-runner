import unittest
from surrogate_1.types import ListFunctor

class TestListFunctor(unittest.TestCase):
    def test_fmap(self):
        lf = ListFunctor([1, 2, 3])
        result = lf.fmap(lambda x: x * 2)
        self.assertEqual(result.items, [2, 4, 6])

if __name__ == "__main__":
    unittest.main()