# at bottom of surrogate/providers/openai.py
from . import register
register("openai", OpenAIProvider)