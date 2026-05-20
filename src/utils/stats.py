import numpy as np
from typing import List, Tuple, Optional

def calculate_mean(data: List[float]) -> float:
    """Calculate the arithmetic mean of a list of numbers."""
    if not data:
        return 0.0
    return sum(data) / len(data)

def calculate_std(data: List[float]) -> float:
    """Calculate the population standard deviation of a list of numbers."""
    if not data:
        return 0.0
    mean_val = calculate_mean(data)
    variance = sum((x - mean_val) ** 2 for x in data) / len(data)
    return np.sqrt(variance)

def rolling_mean(data: List[float], window: int) -> List[float]:
    """Compute the rolling mean with a given window size."""
    if window <= 0:
        return data.copy()
    return [sum(data[i:i+window]) / window for i in range(len(data) - window + 1)]

def rolling_std(data: List[float], window: int) -> List[float]:
    """Compute the rolling standard deviation with a given window size."""
    if window <= 0:
        return data.copy()
    means = rolling_mean(data, window)
    return [calculate_std(data[i:i+window]) for i in range(len(data) - window + 1)]