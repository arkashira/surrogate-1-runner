from typing import Callable
from datetime import datetime
import requests
import os
from src.usage.metrics import record_usage

class LLMCallMiddleware:
    def __init__(self, get_response: Callable[[request], response]):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if 'llm_call' in request.path:
            model = request.headers.get('X-LLM-Model')
            endpoint = request.path
            token_count = int(request.headers.get('X-Token-Count', 0))
            cost = float(request.headers.get('X-Cost', 0.0))

            record_usage(model, endpoint, token_count, cost, request.user.id, request.team.id)

        return response