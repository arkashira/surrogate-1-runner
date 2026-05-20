import pytest
from unittest.mock import MagicMock, patch

# Import the protection logic from the surrogate-1 package.
# It is expected that the package exposes a `protect_trade` function
# that accepts a bot API instance and a dictionary of trade parameters.
try:
    from surrogate_1.protection import protect_trade
except ImportError:
    # If the function is not available, the tests will fail.
    # The implementation of `protect_trade` is part of the surrogate-1
    # library and should be provided by the main codebase.
    raise ImportError("surrogate_1.protection.protect_trade not found")

# ----------------------------------------------------------------------
# Helper fixtures
# ----------------------------------------------------------------------
@pytest.fixture
def trade_params():
    """Sample trade parameters used across tests."""
    return {
        "symbol": "BTC/USDT",
        "side": "buy",
        "type": "limit",
        "amount": 0.01,
        "price": 30000,
    }

# ----------------------------------------------------------------------
# CCXT integration test
# ----------------------------------------------------------------------
def test_ccxt_integration(trade_params):
    """
    Verify that `protect_trade` correctly interacts with a CCXT
    exchange instance by calling `create_order` with the expected
    arguments.
    """
    # Create a mock CCXT exchange with a create_order method.
    mock_exchange = MagicMock()
    mock_exchange.create_order.return_value = {"id": "12345", "status": "open"}

    # Call protect_trade with the mock exchange.
    result = protect_trade(mock_exchange, trade_params)

    # Ensure create_order was called once with the correct parameters.
    mock_exchange.create_order.assert_called_once_with(
        symbol=trade_params["symbol"],
        type=trade_params["type"],
        side=trade_params["side"],
        amount=trade_params["amount"],
        price=trade_params["price"],
    )

    # The result should be the order dict returned by CCXT.
    assert result == {"id": "12345", "status": "open"}

# ----------------------------------------------------------------------
# Freqtrade integration test
# ----------------------------------------------------------------------
def test_freqtrade_integration(trade_params):
    """
    Verify that `protect_trade` correctly interacts with a Freqtrade
    bot instance by calling `place_order` with the expected arguments.
    """
    # Create a mock Freqtrade bot with a place_order method.
    mock_bot = MagicMock()
    mock_bot.place_order.return_value = {"order_id": "abcde", "status": "submitted"}

    # Call protect_trade with the mock bot.
    result = protect_trade(mock_bot, trade_params)

    # Ensure place_order was called once with the correct parameters.
    mock_bot.place_order.assert_called_once_with(
        symbol=trade_params["symbol"],
        side=trade_params["side"],
        type=trade_params["type"],
        amount=trade_params["amount"],
        price=trade_params["price"],
    )

    # The result should be the order dict returned by Freqtrade.
    assert result == {"order_id": "abcde", "status": "submitted"}

# ----------------------------------------------------------------------
# Unsupported bot integration test
# ----------------------------------------------------------------------
def test_unsupported_bot_integration(trade_params):
    """
    Verify that passing an unsupported bot type raises a ValueError.
    """
    # Create a dummy object that does not implement the expected API.
    class DummyBot:
        pass

    dummy_bot = DummyBot()

    with pytest.raises(ValueError) as excinfo:
        protect_trade(dummy_bot, trade_params)

    assert "Unsupported bot API" in str(excinfo.value)

# ----------------------------------------------------------------------
# Configuration loading test
# ----------------------------------------------------------------------
def test_config_loading():
    """
    Ensure that the surrogate-1 configuration can be loaded
    and contains the expected keys for bot integration.
    """
    # The configuration is expected to be available via
    # surrogate_1.config.get_config()
    try:
        from surrogate_1.config import get_config
    except ImportError:
        pytest.skip("surrogate_1.config.get_config not available")

    config = get_config()
    # The config should at least contain a 'bot_protection' section.
    assert isinstance(config, dict)
    assert "bot_protection" in config
    # The bot_protection section should specify a list of supported bots.
    assert isinstance(config["bot_protection"].get("supported_bots", []), list)