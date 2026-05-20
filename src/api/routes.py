from flask import Blueprint, request, jsonify
from functools import wraps
import time
import hashlib

from src.services.usage_service import UsageService
from src.config import CACHE_DURATION_SECONDS

usage_bp = Blueprint('usage', __name__, url_prefix='/api/usage')

def cache_response(duration: int):
    """Decorator to cache API responses for specified duration."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cache_key = hashlib.md5(
                f"{request.method}{request.path}{request.query_string.decode()}"
            ).hexdigest()
            cache_duration = kwargs.get('cache_duration', CACHE_DURATION_SECONDS)
            
            # Check cache (simplified - in production use Redis/Memcached)
            cached = get_from_cache(cache_key)
            if cached:
                return jsonify(cached)
            
            result = f(*args, **kwargs)
            if isinstance(result, tuple) and len(result) == 2:
                data, status = result
            else:
                data, status = result, 200
            
            set_to_cache(cache_key, data, cache_duration)
            return result
        return wrapper
    return decorator

def get_from_cache(key: str):
    """Retrieve from cache - placeholder for actual cache implementation."""
    # In production: use Redis or Memcached
    # For now, return None to force DB query
    return None

def set_to_cache(key: str, data: dict, duration: int):
    """Store in cache - placeholder for actual cache implementation."""
    # In production: use Redis or Memcached
    # TTL in seconds
    pass

@usage_bp.route('/summary', methods=['GET'])
@cache_response(CACHE_DURATION_SECONDS)
def get_usage_summary():
    """
    GET /api/usage/summary
    
    Returns usage summary for the last 30 days with:
    - Total tokens
    - Total cost
    - Breakdown by model
    
    Query parameters:
    - team: optional team filter
    - start_date: optional start date (YYYY-MM-DD)
    - end_date: optional end date (YYYY-MM-DD)
    """
    # Extract filters
    team = request.args.get('team')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Default to last 30 days if no dates provided
    from datetime import datetime, timedelta
    if not start_date:
        end_dt = datetime.utcnow()
        start_dt = end_dt - timedelta(days=30)
        start_date = start_dt.strftime('%Y-%m-%d')
        end_date = end_dt.strftime('%Y-%m-%d')
    
    # Get usage data
    usage_service = UsageService()
    summary = usage_service.get_summary(
        team=team,
        start_date=start_date,
        end_date=end_date
    )
    
    return jsonify({
        'total_tokens': summary['total_tokens'],
        'total_cost': summary['total_cost'],
        'currency': summary['currency'],
        'period': {
            'start_date': summary['period']['start_date'],
            'end_date': summary['period']['end_date']
        },
        'breakdown_by_model': summary['breakdown_by_model'],
        'breakdown_by_team': summary['breakdown_by_team']
    })