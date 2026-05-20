import time
import redis
from functools import wraps
from flask import request, Response, jsonify

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def rate_limit(limit=100, period=60):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            if not api_key:
                return jsonify({"error": "API key required"}), 400
            
            key = f"rate_limit:{api_key}"
            now = int(time.time())
            pipe = redis_client.pipeline()
            
            # Remove tokens older than the current period
            pipe.zremrangebyscore(key, '-inf', now - period)
            
            # Get the number of tokens in the current period
            remaining = limit - pipe.zcard(key)
            pipe.execute()
            
            if remaining <= 0:
                reset_time = redis_client.zrange(key, -1, -1, withscores=True)
                if reset_time:
                    reset_time = reset_time[0][1]
                else:
                    reset_time = now + period
                
                headers = {
                    'Retry-After': str(reset_time - now),
                    'X-RateLimit-Limit': str(limit),
                    'X-RateLimit-Remaining': '0',
                    'X-RateLimit-Reset': str(reset_time)
                }
                
                return Response("Rate limit exceeded", status=429, headers=headers)
            
            # Add the current request to the set
            redis_client.zadd(key, {str(now): now})
            redis_client.expire(key, period)
            
            response = f(*args, **kwargs)
            response.headers['X-RateLimit-Limit'] = str(limit)
            response.headers['X-RateLimit-Remaining'] = str(remaining - 1)
            response.headers['X-RateLimit-Reset'] = str(now + period)
            
            # Log the rate limit event
            log_rate_limit_event(api_key, now)
            
            return response
        
        return wrapped
    
    return decorator

def log_rate_limit_event(api_key, timestamp):
    # Implement logging mechanism here
    print(f"Rate limit event: API Key={api_key}, Timestamp={timestamp}")