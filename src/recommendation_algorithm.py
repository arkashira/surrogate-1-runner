import csv
import os
from typing import Dict, List, Optional, Tuple

# Path to the CSV containing component data
GAME_DATA_CSV = os.path.join(os.path.dirname(__file__), "game_data.csv")

# Hard‑coded game requirement profiles
GAME_REQUIREMENTS: Dict[str, Dict[str, float]] = {
    "Cyberpunk 2077": {"cpu_score": 8.0, "gpu_score": 8.0, "ram_gb": 16, "storage_gb": 512},
    "Minecraft": {"cpu_score": 4.0, "gpu_score": 4.0, "ram_gb": 8, "storage_gb": 256},
    "Fortnite": {"cpu_score": 5.0, "gpu_score": 5.0, "ram_gb": 8, "storage_gb": 256},
    # Add more games as needed
}

def _load_components() -> List[Dict]:
    """
    Load component data from the CSV file.
    Each row must contain:
        component_type, name, price, cpu_score, gpu_score, ram_gb, storage_gb
    """
    components = []
    with open(GAME_DATA_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields
            row["price"] = float(row["price"])
            row["cpu_score"] = float(row["cpu_score"])
            row["gpu_score"] = float(row["gpu_score"])
            row["ram_gb"] = float(row["ram_gb"])
            row["storage_gb"] = float(row["storage_gb"])
            components.append(row)
    return components

def _best_component(
    components: List[Dict],
    comp_type: str,
    requirement: float,
    current_value: float,
    attr: str,
) -> Optional[Tuple[Dict, float]]:
    """
    Return the cheapest component of type `comp_type` that meets or exceeds
    the requirement `requirement` for attribute `attr`. If the current value
    already satisfies the requirement, return None.
    """
    if current_value >= requirement:
        return None, 0.0
    candidates = [
        c for c in components if c["component_type"] == comp_type and c[attr] >= requirement
    ]
    if not candidates:
        return None, 0.0
    best = min(candidates, key=lambda c: c["price"])
    return best, best["price"]

def recommend_components(
    budget: float,
    target_game: str,
    current_hardware: Dict[str, float],
) -> Optional[Dict]:
    """
    Recommend a component mix for the given budget and target game.

    Parameters
    ----------
    budget : float
        Maximum total price allowed for the recommendation.
    target_game : str
        Name of the target game.
    current_hardware : dict
        Dictionary containing current hardware specs:
            cpu_score, gpu_score, ram_gb, storage_gb

    Returns
    -------
    dict or None
        Dictionary with keys:
            cpu, gpu, ram, storage, total_price
        Each component is a dict from the CSV. If no feasible mix exists,
        returns None.
    """
    if target_game not in GAME_REQUIREMENTS:
        raise ValueError(f"Unknown game: {target_game}")

    req = GAME_REQUIREMENTS[target_game]
    components = _load_components()

    recommendation = {}
    total_price = 0.0

    # CPU
    cpu, cpu_price = _best_component(
        components,
        "CPU",
        req["cpu_score"],
        current_hardware.get("cpu_score", 0.0),
        "cpu_score",
    )
    if cpu:
        recommendation["cpu"] = cpu
        total_price += cpu_price

    # GPU
    gpu, gpu_price = _best_component(
        components,
        "GPU",
        req["gpu_score"],
        current_hardware.get("gpu_score", 0.0),
        "gpu_score",
    )
    if gpu:
        recommendation["gpu"] = gpu
        total_price += gpu_price

    # RAM
    ram, ram_price = _best_component(
        components,
        "RAM",
        req["ram_gb"],
        current_hardware.get("ram_gb", 0.0),
        "ram_gb",
    )
    if ram:
        recommendation["ram"] = ram
        total_price += ram_price

    # Storage
    storage, storage_price = _best_component(
        components,
        "Storage",
        req["storage_gb"],
        current_hardware.get("storage_gb", 0.0),
        "storage_gb",
    )
    if storage:
        recommendation["storage"] = storage
        total_price += storage_price

    if total_price > budget:
        # Budget exceeded; no recommendation possible
        return None

    recommendation["total_price"] = total_price
    return recommendation