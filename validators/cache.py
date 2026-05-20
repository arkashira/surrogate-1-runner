import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# Constants
MAX_TTL_SECONDS = 31536000  # 1 year
MIN_TTL_SECONDS = 0
RECOMMENDED_MIN_TTL = 60   # 1 minute
DEFAULT_WARN_TTL_HIGH = 604800  # 1 week

@dataclass
class CacheValidationResult:
    is_valid: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    
    def add_warning(self, message: str) -> None:
        self.warnings.append(message)
        logger.warning(message)
    
    def add_error(self, message: str) -> None:
        self.errors.append(message)
        self.is_valid = False
        logger.error(message)

def validate_cache_policy(config: Dict[str, Any]) -> CacheValidationResult:
    """
    Validates cache policy configuration for behaviors.
    
    Args:
        config: Dictionary containing behavior configuration
        
    Returns:
        CacheValidationResult with validation status and messages
    """
    result = CacheValidationResult(is_valid=True)
    
    # Check if cache policy exists
    if 'cache_policy' not in config:
        result.add_error("Cache policy is missing from behavior configuration")
        
        # Check for deprecated ViewerProtocolPolicy usage
        if 'viewer_protocol_policy' in config:
            result.add_error(
                "Deprecated ViewerProtocolPolicy detected. Use cache policy instead."
            )
        return result
    
    cache_policy = config['cache_policy']
    
    # Validate cache TTL settings
    if 'ttl' in cache_policy:
        ttl = cache_policy['ttl']
        
        # Type validation
        if not isinstance(ttl, (int, float)):
            result.add_error(f"Invalid TTL type: {type(ttl).__name__}. Expected int or float.")
            return result
        
        # Range validation
        if ttl < MIN_TTL_SECONDS:
            result.add_error(f"Cache TTL cannot be negative: {ttl}")
        elif ttl > MAX_TTL_SECONDS:
            result.add_warning(
                f"Cache TTL exceeds 1 year ({ttl}s). This may cause unnecessary costs."
            )
        elif ttl > DEFAULT_WARN_TTL_HIGH:
            result.add_warning(
                f"Cache TTL is very high ({ttl}s). Consider reducing for better invalidation."
            )
        elif ttl < RECOMMENDED_MIN_TTL:
            result.add_warning(
                f"Cache TTL is very low ({ttl}s). May impact performance negatively."
            )
    
    # Validate minimum TTL if specified
    if 'min_ttl' in cache_policy:
        min_ttl = cache_policy['min_ttl']
        if not isinstance(min_ttl, (int, float)):
            result.add_error(f"Invalid min_ttl type: {type(min_ttl).__name__}. Expected int or float.")
        elif min_ttl < 0:
            result.add_error(f"min_ttl cannot be negative: {min_ttl}")
    
    # Check for origin cache headers
    if 'origin_cache_headers' not in cache_policy:
        result.add_warning(
            "Missing origin_cache_headers. Consider adding cache headers for better performance."
        )
    else:
        origin_headers = cache_policy['origin_cache_headers']
        
        if not isinstance(origin_headers, dict):
            result.add_error("origin_cache_headers must be a dictionary.")
        else:
            # Check for common required headers
            required_headers = ['Cache-Control']
            recommended_headers = ['Expires', 'ETag', 'Last-Modified']
            
            for header in required_headers:
                if header not in origin_headers:
                    result.add_error(f"Missing required origin cache header: {header}")
            
            for header in recommended_headers:
                if header not in origin_headers:
                    result.add_warning(f"Missing recommended origin cache header: {header}")
    
    # Validate compress flag if present
    if 'compress' in cache_policy:
        if not isinstance(cache_policy['compress'], bool):
            result.add_error("'compress' must be a boolean value.")
    
    logger.info(
        f"Cache validation complete: valid={result.is_valid}, "
        f"errors={len(result.errors)}, warnings={len(result.warnings)}"
    )
    
    return result