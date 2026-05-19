# <repo_root>/test_configurations/filter_tests.py
# -------------------------------------------------
# Public API:
#   - create_env_var_filter(env_var_name) -> Callable[[str], bool]
#   - get_filtered_tests(test_names, filters) -> List[str]
# -------------------------------------------------
import os
from typing import List, Callable


class TestFilter:
    """
    Holds a collection of predicate functions (filters) and decides whether a
    test name satisfies *all* of them.
    """
    def __init__(self, filters: List[Callable[[str], bool]]):
        self.filters = filters

    def should_run_test(self, test_name: str) -> bool:
        """Return True only if every filter returns True for ``test_name``."""
        return all(filter_fn(test_name) for filter_fn in self.filters)


def create_env_var_filter(env_var_name: str) -> Callable[[str], bool]:
    """
    Build a filter that checks whether the value of ``env_var_name`` appears
    (case‑insensitively) in the test name.

    Example:
        os.environ["TARGET"] = "login"
        f = create_env_var_filter("TARGET")
        f("TestLoginSuccess")   # → True
        f("TestLogout")         # → False
    """
    env_value = os.getenv(env_var_name, '').lower()

    def filter_fn(test_name: str) -> bool:
        # Empty env var means “no restriction” – the filter always passes.
        if not env_value:
            return True
        return env_value in test_name.lower()

    return filter_fn


def get_filtered_tests(
    test_names: List[str],
    filters: List[Callable[[str], bool]],
) -> List[str]:
    """
    Apply the supplied ``filters`` to ``test_names`` and return the subset that
    should be executed.
    """
    test_filter = TestFilter(filters)
    return [name for name in test_names if test_filter.should_run_test(name)]