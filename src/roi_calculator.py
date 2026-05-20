import time
import hashlib
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ComponentSpec:
    """Represents a component specification with performance and cost metrics."""
    fps: float
    price: float


@dataclass
class RoiResult:
    """Represents the result of ROI calculation."""
    current: ComponentSpec
    proposed: ComponentSpec
    gain: float
    price_diff: float
    roi: float


class RoiCalculator:
    """Calculates FPS gain and ROI for component upgrades with caching."""
    
    def __init__(self, cache_ttl: int = 300):
        """
        Initialize the ROI calculator.
        
        Args:
            cache_ttl: Cache time-to-live in seconds (default 5 minutes)
        """
        self.cache_ttl = cache_ttl
        self._cache: Dict[str, tuple] = {}
    
    def _generate_cache_key(self, current_spec: ComponentSpec, 
                          proposed_spec: ComponentSpec) -> str:
        """
        Generate a cache key based on component specs.
        
        Args:
            current_spec: Current component specification
            proposed_spec: Proposed component specification
            
        Returns:
            Hashed cache key string
        """
        key_string = f"{current_spec.fps}:{current_spec.price}:{proposed_spec.fps}:{proposed_spec.price}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_time: float) -> bool:
        """
        Check if cached entry is still valid.
        
        Args:
            cache_time: Time when entry was cached
            
        Returns:
            True if cache is valid, False otherwise
        """
        return time.time() - cache_time < self.cache_ttl
    
    def calculate_roi(self, current_spec: ComponentSpec, 
                     proposed_spec: ComponentSpec) -> RoiResult:
        """
        Calculate FPS gain and ROI for component upgrade.
        
        Args:
            current_spec: Current component specification
            proposed_spec: Proposed component specification
            
        Returns:
            RoiResult containing all calculated values
        """
        # Check cache for existing result
        cache_key = self._generate_cache_key(current_spec, proposed_spec)
        if cache_key in self._cache:
            cached_time, cached_result = self._cache[cache_key]
            if self._is_cache_valid(cached_time):
                return cached_result
        
        # Calculate FPS gain
        fps_gain = proposed_spec.fps - current_spec.fps
        
        # Calculate price difference
        price_diff = proposed_spec.price - current_spec.price
        
        # Calculate ROI (avoid negative ROI)
        roi = max(0.0, fps_gain / price_diff) if price_diff != 0 else 0.0
        roi = round(roi, 2)
        
        # Create result object
        result = RoiResult(
            current=current_spec,
            proposed=proposed_spec,
            gain=fps_gain,
            price_diff=price_diff,
            roi=roi
        )
        
        # Store in cache
        self._cache[cache_key] = (time.time(), result)
        
        return result