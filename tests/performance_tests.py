"""
Performance testing suite for the surrogate-1 parser.

The tests verify that the parser can handle large data streams within
acceptable latency bounds and remains stable under repeated load.

Running these tests with ``pytest`` will output timing information.
"""

import time
import random
import string
from typing import List

import pytest

# Import the parser implementation. Adjust the import path if the parser
# resides elsewhere in the codebase.
try:
    from surrogate_1.parser import parse  # type: ignore
except ImportError as exc:
    raise ImportError(
        "Parser module not found. Ensure that `surrogate_1/parser.py` "
        "exposes a `parse` callable."
    ) from exc


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def _random_word(min_len: int = 5, max_len: int = 12) -> str:
    """Generate a random alphabetic word."""
    length = random.randint(min_len, max_len)
    return "".join(random.choices(string.ascii_letters, k=length))


def generate_large_dataset(num_records: int) -> List[dict]:
    """
    Produce a list of synthetic records that mimics the shape of the real
    dataset processed by the parser.

    Each record is a flat dictionary with a handful of string fields.
    """
    dataset = []
    for _ in range(num_records):
        record = {
            "id": _random_word(),
            "title": _random_word(10, 30),
            "description": _random_word(50, 200),
            "category": random.choice(["news", "blog", "forum", "wiki"]),
            "content": _random_word(200, 1000),
        }
        dataset.append(record)
    return dataset


# ----------------------------------------------------------------------
# Performance benchmarks
# ----------------------------------------------------------------------
# Benchmark thresholds (seconds). Adjust based on hardware and SLA.
MAX_TIME_SECONDS_10MB = 2.5   # Parsing ~10 MiB should finish within 2.5 s
MAX_TIME_SECONDS_100MB = 12.0  # Parsing ~100 MiB should finish within 12 s
STABILITY_ITERATIONS = 20    # Number of repeated runs for stability test


def _measure_parse_time(data: List[dict]) -> float:
    """Run the parser on ``data`` and return elapsed seconds."""
    start = time.perf_counter()
    parse(data)  # The parser is expected to accept a list of dicts.
    end = time.perf_counter()
    return end - start


def test_parser_speed_10mb():
    """
    Verify that parsing a ~10 MiB synthetic dataset completes within the
    defined performance budget.
    """
    # Approximate record size: ~500 bytes → 20 000 records ≈ 10 MiB
    dataset = generate_large_dataset(num_records=20_000)
    elapsed = _measure_parse_time(dataset)
    print(f"[performance] 10 MiB parse time: {elapsed:.3f}s")
    assert elapsed <= MAX_TIME_SECONDS_10MB, (
        f"Parser exceeded time budget: {elapsed:.3f}s > {MAX_TIME_SECONDS_10MB}s"
    )


def test_parser_speed_100mb():
    """
    Verify that parsing a ~100 MiB synthetic dataset completes within the
    defined performance budget.
    """
    # Approximate record size: ~500 bytes → 200 000 records ≈ 100 MiB
    dataset = generate_large_dataset(num_records=200_000)
    elapsed = _measure_parse_time(dataset)
    print(f"[performance] 100 MiB parse time: {elapsed:.3f}s")
    assert elapsed <= MAX_TIME_SECONDS_100MB, (
        f"Parser exceeded time budget: {elapsed:.3f}s > {MAX_TIME_SECONDS_100MB}s"
    )


def test_parser_stability_under_load():
    """
    Run the parser repeatedly on a moderate‑size dataset to ensure no
    degradation, crashes, or memory leaks occur across iterations.
    """
    dataset = generate_large_dataset(num_records=30_000)  # ~15 MiB per run
    timings = []
    for i in range(STABILITY_ITERATIONS):
        elapsed = _measure_parse_time(dataset)
        timings.append(elapsed)
        print(f"[stability] iteration {i+1}/{STABILITY_ITERATIONS}: {elapsed:.3f}s")
        # Basic sanity check: each run must stay within a generous bound.
        assert elapsed < (MAX_TIME_SECONDS_10MB * 2), (
            f"Iteration {i+1} exceeded stability time bound: {elapsed:.3f}s"
        )
    avg_time = sum(timings) / len(timings)
    print(f"[stability] average parse time over {STABILITY_ITERATIONS} runs: {avg_time:.3f}s")