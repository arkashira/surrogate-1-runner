import time
import numpy as np
import pytest
from surrogate.simulation import run_simulation  # Adjust import path as needed


def _generate_dummy_input(num_rows: int) -> np.ndarray:
    """
    Generate deterministic dummy input data for the simulation.
    Schema includes 'price', 'demand_factor', and 'cost'.
    """
    rng = np.random.default_rng(42)
    data = np.zeros(num_rows, dtype=[("price", "f8"), ("demand_factor", "f8"), ("cost", "f8")])
    data["price"] = rng.uniform(5, 50, size=num_rows)
    data["demand_factor"] = rng.uniform(0.5, 1.5, size=num_rows)
    data["cost"] = rng.uniform(1, 10, size=num_rows)
    return data


@pytest.mark.parametrize("num_rows", [10_000])
def test_simulation_latency(num_rows: int):
    """
    Ensure the Monte-Carlo pricing simulation completes within 5 seconds
    for up to 10k input rows.
    """
    seed = 12345
    input_data = _generate_dummy_input(num_rows)

    start = time.perf_counter()
    result = run_simulation(input_data, seed=seed)
    elapsed = time.perf_counter() - start

    assert isinstance(result, dict), "Simulation must return a dict-like result"
    assert elapsed < 5.0, f"Simulation latency {elapsed:.2f}s exceeds 5-second SLA for {num_rows} rows"