import numpy as np
from typing import List, Tuple


def simulate_pricing(
    price_points: List[float],
    demand_means: List[float],
    demand_stds: List[float],
    n_simulations: int = 10_000,
    seed: int = 42,
) -> Tuple[float, float, Tuple[float, float], Tuple[float, float]]:
    """
    Monte‑Carlo simulation of revenue = price × demand.

    Parameters
    ----------
    price_points : List[float]
        Candidate prices to evaluate (must be > 0).
    demand_means : List[float]
        Expected demand for each price point (≥ 0).
    demand_stds : List[float]
        Standard deviation of demand for each price point (≥ 0).
    n_simulations : int, default 10 000
        Number of random draws per price point.
    seed : int, default 42
        Random seed for reproducibility.

    Returns
    -------
    optimal_price : float
        Price that yields the highest *expected* revenue.
    expected_revenue : float
        Mean revenue at the optimal price.
    ci_95 : Tuple[float, float]
        95 % confidence interval for the optimal revenue (percentile‑based).
    price_range : Tuple[float, float]
        Smallest contiguous price interval whose expected revenue is within
        1 % of the maximum expected revenue.
    """
    # ------------------------------------------------------------------ #
    # 1️⃣ Input sanity – defensive programming (mirrors Pydantic validation) #
    # ------------------------------------------------------------------ #
    if not (len(price_points) == len(demand_means) == len(demand_stds)):
        raise ValueError("All input lists must have the same length.")
    if any(p <= 0 for p in price_points):
        raise ValueError("All price points must be > 0.")
    if any(m < 0 for m in demand_means):
        raise ValueError("Demand means must be >= 0.")
    if any(s < 0 for s in demand_stds):
        raise ValueError("Demand stds must be >= 0.")
    if n_simulations <= 0:
        raise ValueError("n_simulations must be a positive integer.")

    rng = np.random.default_rng(seed)

    # --------------------------------------------------------------- #
    # 2️⃣ Simulate demand → revenue for every price point
    # --------------------------------------------------------------- #
    revenues = np.empty((len(price_points), n_simulations), dtype=np.float64)

    for i, (mean, std) in enumerate(zip(demand_means, demand_stds)):
        # Normal demand, truncated at 0 (no negative demand)
        demand_samples = rng.normal(loc=mean, scale=std, size=n_simulations)
        demand_samples = np.clip(demand_samples, a_min=0, a_max=None)
        revenues[i] = price_points[i] * demand_samples

    # --------------------------------------------------------------- #
    # 3️⃣ Summarise results
    # --------------------------------------------------------------- #
    exp_rev = revenues.mean(axis=1)                     # expected revenue per price
    lower = np.percentile(revenues, 2.5, axis=1)        # 2.5th percentile → lower CI
    upper = np.percentile(revenues, 97.5, axis=1)       # 97.5th percentile → upper CI

    opt_idx = int(np.argmax(exp_rev))
    optimal_price = price_points[opt_idx]
    expected_revenue = exp_rev[opt_idx]
    ci_95 = (float(lower[opt_idx]), float(upper[opt_idx]))

    # --------------------------------------------------------------- #
    # 4️⃣ Price range whose expected revenue is within 1 % of the max
    # --------------------------------------------------------------- #
    threshold = expected_revenue * 0.99
    eligible = np.where(exp_rev >= threshold)[0]
    price_range = (float(price_points[eligible[0]]), float(price_points[eligible[-1]]))

    return optimal_price, expected_revenue, ci_95, price_range