"""
Integration tests for the `dynamic_workspace_id_config` module.

The tests verify that:

1.  A configuration object can be retrieved.
2.  The configuration can be injected into an existing workflow.
3.  Retrieving the configuration is fast enough to not become a bottleneck.

The tests use `unittest.mock` to avoid touching the real workflow engine
and to keep the tests deterministic.
"""

import time
import unittest
from unittest.mock import patch, MagicMock

# Import the module under test
from surrogate_1 import dynamic_workspace_id_config


class TestDynamicWorkspaceIDConfig(unittest.TestCase):
    """Test suite for dynamic workspace ID configuration."""

    # ------------------------------------------------------------------
    # 1.  Configuration retrieval
    # ------------------------------------------------------------------
    def test_dynamic_workspace_id_config(self):
        """`get_config()` should return a non‑None object."""
        config = dynamic_workspace_id_config.get_config()
        self.assertIsNotNone(
            config,
            msg="get_config() returned None – configuration was not created."
        )

    # ------------------------------------------------------------------
    # 2.  Integration with an existing workflow
    # ------------------------------------------------------------------
    @patch("surrogate_1.existing_workflow")
    def test_integration_with_existing_workflows(self, mock_workflow):
        """
        `integrate_with_workflow()` should call the existing workflow
        exactly once with the configuration object.
        """
        # Arrange – the mock returns a dummy workflow object
        mock_workflow.return_value = MagicMock(name="DummyWorkflow")

        # Act – perform the integration
        dynamic_workspace_id_config.integrate_with_workflow()

        # Assert – the workflow was invoked once
        mock_workflow.assert_called_once_with(
            dynamic_workspace_id_config.get_config()
        )

    # ------------------------------------------------------------------
    # 3.  Performance guard
    # ------------------------------------------------------------------
    def test_performance(self):
        """
        Retrieving the configuration should be quick.
        The threshold is intentionally generous (1 s) but will surface
        obvious regressions.
        """
        start = time.perf_counter()
        dynamic_workspace_id_config.get_config()
        elapsed = time.perf_counter() - start

        # Use a custom message to aid debugging if the test fails
        self.assertLess(
            elapsed,
            1.0,
            msg=f"Configuration retrieval took {elapsed:.3f}s, exceeding the 1 s threshold."
        )


# ----------------------------------------------------------------------
# The following block allows the test to be run directly with
# `python -m unittest import_test.py` or via `pytest`.
# ----------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()