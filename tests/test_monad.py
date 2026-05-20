from python_hkt.monad import Monad, Maybe

def test_monad_bind_and_map():
    m = Maybe.unit(5)
    result = m.bind(lambda x: Maybe.unit(x + 1)).map(lambda x: x * 2)
    assert isinstance(result, Maybe)
    assert result.value == 12

def test_monad_with_none():
    n = Maybe.unit(None)
    result = n.bind(lambda x: Maybe.unit(x + 1))
    assert isinstance(result, Maybe)
    assert result.value is None