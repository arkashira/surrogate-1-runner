class MonadValidator:
    def validate_monad_laws(self, m: 'Monad') -> bool:
        # Check left identity law
        return (m.bind(lambda x: x, lambda _: m.unit(1)) == m.unit(1))

    def validate_right_identity(self, m: 'Monad') -> bool:
        # Check right identity law
        return (m.bind(lambda x: m.unit(x), lambda _: x) == m.unit(x))

    def validate_associativity(self, m: 'Monad') -> bool:
        # Check associativity law
        return (m.bind(lambda x: m.bind(lambda y: m.unit(x + y), lambda z: z), lambda w: w) == m.bind(lambda x: m.bind(lambda y: m.unit(x + y), lambda z: m.bind(lambda w: m.unit(z + w), lambda v: v)), lambda u: u))

class Monad:
    def bind(self, f, g):
        raise NotImplementedError

    def unit(self, value):
        raise NotImplementedError