import asyncio
import pytest
from src.render.async_handler import AsyncHandler

@pytest.mark.asyncio
async def test_submit_render_job():
    handler = AsyncHandler()

    async def mock_render_job(frame_data):
        await asyncio.sleep(0.016)  # Simulating 16ms latency
        return "Rendered Frame"

    future = handler.submit_render_job(mock_render_job, "Frame Data")
    result = await handler.handle_result(future)
    assert result == "Rendered Frame"

def error_callback(exception):
    print(f"Error occurred: {exception}")

@pytest.mark.asyncio
async def test_error_handling():
    handler = AsyncHandler()
    handler.add_error_callback(error_callback)

    async def failing_render_job():
        await asyncio.sleep(0.016)  # Simulating 16ms latency
        raise Exception("GPU Failure")

    future = handler.submit_render_job(failing_render_job)
    with pytest.raises(Exception):
        await handler.handle_result(future)