import unittest
from surrogate_1.monad_instances import Maybe, List


class TestMaybe(unittest.TestCase):
    def test_just(self):
        m = Maybe.just(5)
        self.assertEqual(m.value, 5)

    def test_nothing(self):
        m = Maybe.nothing()
        self.assertIsNone(m.value)

    def test_bind_with_value(self):
        m = Maybe.just(5)
        result = m.bind(lambda x: Maybe.just(x + 1))
        self.assertEqual(result.value, 6)

    def test_bind_with_nothing(self):
        m = Maybe.nothing()
        result = m.bind(lambda x: Maybe.just(x + 1))
        self.assertIsNone(result.value)


class TestList(unittest.TestCase):
    def test_bind(self):
        l = List([1, 2, 3])
        result = l.bind(lambda x: List.from_value(x + 1))
        self.assertEqual(result.values, [2, 3, 4])

    def test_empty_list(self):
        l = List.empty()
        result = l.bind(lambda x: List.from_value(x + 1))
        self.assertEqual(result.values, [])


if __name__ == '__main__':
    unittest.main()