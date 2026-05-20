from aiohttp import web
import json

API_KEY = "sk_test_123456"  # Replace with actual API key

async def auth_middleware(request):
    headers = request.headers.get('x-api-key')
    if not headers or headers != API_KEY:
        return web.Response(status=401, text="Unauthorized")
    return None

app = web.Application(middlewares=[auth_middleware])