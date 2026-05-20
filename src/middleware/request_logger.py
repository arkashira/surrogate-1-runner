import time
import logging
from flask import request, g
from functools import wraps
from ..utils.data_sanitizer import sanitize_data
from ..utils.compliance_checker import check_compliance

logger = logging.getLogger(__name__)

def log_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        response = f(*args, **kwargs)
        latency = (time.time() - start_time) * 1000  # Convert to milliseconds

        if latency > 100:
            log_data = {
                'method': request.method,
                'path': request.path,
                'latency': latency,
                'status_code': response.status_code,
                'user_agent': request.headers.get('User-Agent'),
                'ip_address': request.remote_addr
            }
            logger.info(f"High latency request: {log_data}")

        return response
    return decorated_function

def log_compliance(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_data = request.get_json()
        sanitized_data = sanitize_data(request_data)
        compliance_status = check_compliance(sanitized_data)

        if not compliance_status['is_compliant']:
            log_data = {
                'method': request.method,
                'path': request.path,
                'status_code': 400,
                'non_compliant_data': compliance_status['non_compliant_fields'],
                'user_agent': request.headers.get('User-Agent'),
                'ip_address': request.remote_addr
            }
            logger.warning(f"Non-compliant request: {log_data}")

        return f(*args, **kwargs)
    return decorated_function