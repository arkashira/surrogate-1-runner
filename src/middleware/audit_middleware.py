from functools import wraps
from flask import request, g
from audit_logger import AuditLogger

audit_logger = AuditLogger()

def audit_log_middleware():
    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            # Extract request metadata
            request_id = request.headers.get('X-Request-ID', 'unknown')
            user_id = g.user.id if hasattr(g, 'user') else 'anonymous'
            model = request.args.get('model', 'unknown')
            endpoint = request.path
            tunnel_used = request.headers.get('X-Tunnel-Used', 'false').lower() == 'true'
            
            # Execute original function
            response = f(*args, **kwargs)
            
            # Log with actual response status code
            audit_logger.log_request(
                request_id=request_id,
                user_id=user_id,
                model=model,
                endpoint=endpoint,
                tunnel_used=tunnel_used,
                response_status=response.status_code
            )
            
            return response
        return wrapped_function
    return decorator