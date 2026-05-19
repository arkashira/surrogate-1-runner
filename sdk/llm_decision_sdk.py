import aiohttp
import asyncio

class DecisionError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

async def decide(input_data: dict) -> dict:
    url = "https://api.example.com/decide"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=input_data, timeout=10) as response:
                if response.status != 200:
                    raise DecisionError(f"API returned status {response.status}", response.status)
                return await response.json()
    except aiohttp.ClientError as e:
        raise DecisionError(f"Network error: {str(e)}")
    except asyncio.TimeoutError:
        raise DecisionError("Request timed out")

# Example usage
if __name__ == "__main__":
    input_data = {"key": "value"}
    result = asyncio.run(decide(input_data))
    print(result)