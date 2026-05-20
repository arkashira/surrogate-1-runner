class MaybeMonad(Monad):
    def __init__(self, value=None):
        self.value = value

    def bind(self, f, g):
        if self.value is None:
            return g(None)
        else:
            return f(self.value)

    def unit(self, value):
        return MaybeMonad(value)