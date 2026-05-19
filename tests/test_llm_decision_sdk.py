import pytest
from unittest.mock import AsyncMock, patch
from sdk.llm_decision_sdk import decide, DecisionError

@pytest.mark.asyncio
async def test_decide_success():
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {"result": "success"}
    
    with patch('aiohttp.ClientSession.post', return_value=mock_response):
        result = await decide({"key": "value"})
        assert result == {"result": "success"}

@pytest.mark.asyncio
async def test_decide_network_error():
    with patch('aiohttp.ClientSession.post', side_effect=aiohttp.ClientError("Network issue")):
        with pytest.raises(DecisionError) as exc_info:
            await decide({"key": "value"})
        assert str(exc_info.value) == "Network error: Network issue"

@pytest.mark.asyncio
async def test_decide_timeout():
    with patch('aiohttp.ClientSession.post', side_effect=asyncio.TimeoutError()):
        with pytest.raises(DecisionError) as exc_info:
            await decide({"key": "value"})
        assert str(exc_info.value) == "Request timed out"