class Monad:
    def bind(self, func):
        raise NotImplementedError("Bind method not implemented.")

    def __rshift__(self, func):
        return self.bind(func)


class Maybe(Monad):
    def __init__(self, value):
        self.value = value

    def is_nothing(self):
        return self.value is None

    def bind(self, func):
        if self.is_nothing():
            return Maybe(None)
        return func(self.value)

    @staticmethod
    def just(value):
        return Maybe(value)

    @staticmethod
    def nothing():
        return Maybe(None)


class List(Monad):
    def __init__(self, values):
        self.values = values

    def bind(self, func):
        return List([result for value in self.values for result in func(value).values])

    @staticmethod
    def from_value(value):
        return List([value])

    @staticmethod
    def empty():
        return List([])