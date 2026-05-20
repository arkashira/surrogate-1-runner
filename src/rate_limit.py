from slowapi import Limiter
from slowapi.util import get_remote_address

# The key function extracts the client IP (or any other identifier you prefer)
limiter = Limiter(key_func=get_remote_address)