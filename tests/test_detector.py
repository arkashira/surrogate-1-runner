import json
import os
import subprocess
import sys
import time
import tempfile
import pytest
from pathlib import Path

# Constants
MAX_LATENCY_MS = 200
TEST_DATA_DIR = Path(__file__).parent / "test_data"

# Baseline signatures for testing
BASELINE_SIGNATURES = {
    "api-gateway:v1": {
        "method": "POST",
        "path": "/api/v1/users",
        "required_headers": ["Authorization", "Content-Type", "X-Request-ID"],
        "json_schema": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "email": {"type": "string", "format": "email"}
            },
            "required": ["username", "email"]
        }
    }
}

def _run_detector(baseline: dict, new: dict) -> subprocess.CompletedProcess:
    """Helper to run detector with temporary files and measure performance."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as baseline_file, \
         tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as new_file:

        json.dump(baseline, baseline_file)
        baseline_file.flush()
        json.dump(new, new_file)
        new_file.flush()

        start_time = time.perf_counter()
        result = subprocess.run(
            [sys.executable, "-m", "surrogate_1.detector", baseline_file.name, new_file.name],
            capture_output=True,
            text=True,
            timeout=5
        )
        duration_ms = (time.perf_counter() - start_time) * 1000

        # Clean up
        os.unlink(baseline_file.name)
        os.unlink(new_file.name)

        # Verify performance
        assert duration_ms <= MAX_LATENCY_MS, f"Detection took {duration_ms:.1f}ms > {MAX_LATENCY_MS}ms"

        return result

@pytest.fixture
def baseline_file(tmp_path):
    """Create a temporary baseline file with test signatures."""
    baseline_path = tmp_path / "baseline.json"
    with open(baseline_path, "w") as f:
        json.dump(BASELINE_SIGNATURES, f, indent=2)
    return baseline_path

class TestDriftDetection:
    """Comprehensive integration tests for drift detection."""

    def test_detector_exists(self):
        """Verify detector module exists."""
        detector_path = Path(sys.modules["surrogate_1.detector"].__file__)
        assert detector_path.exists(), f"Detector module not found at {detector_path}"

    def test_pass_identical_signatures(self):
        """Test PASS when signatures are identical."""
        baseline = BASELINE_SIGNATURES["api-gateway:v1"]
        result = _run_detector(baseline, baseline.copy())

        assert result.returncode == 0, f"Expected PASS (exit 0), got {result.returncode}"
        assert "PASS" in result.stdout, f"Expected PASS in output, got: {result.stdout}"

    def test_fail_method_change(self):
        """Test FAIL when HTTP method changes."""
        baseline = BASELINE_SIGNATURES["api-gateway:v1"]
        new = baseline.copy()
        new["method"] = "GET"

        result = _run_detector(baseline, new)

        assert result.returncode == 1, f"Expected FAIL (exit 1), got {result.returncode}"
        assert "FAIL" in result.stdout, f"Expected FAIL in output, got: {result.stdout}"

    def test_fail_path_change(self):
        """Test FAIL when path changes."""
        baseline = BASELINE_SIGNATURES["api-gateway:v1"]
        new = baseline.copy()
        new["path"] = "/api/v2/users"

        result = _run_detector(baseline, new)

        assert result.returncode == 1, f"Expected FAIL (exit 1), got {result.returncode}"
        assert "FAIL" in result.stdout, f"Expected FAIL in output, got: {result.stdout}"

    def test_fail_missing_required_header(self):
        """Test FAIL when required header is missing."""
        baseline = BASELINE_SIGNATURES["api-gateway:v1"]
        new = baseline.copy()
        new["required_headers"].remove("Authorization")

        result = _run_detector(baseline, new)

        assert result.returncode == 1, f"Expected FAIL (exit 1), got {result.returncode}"
        assert "FAIL" in result.stdout, f"Expected FAIL in output, got: {result.stdout}"

    def test_pass_header_superset(self):
        """Test PASS when incoming has superset of required headers."""
        baseline = BASELINE_SIGNATURES["api-gateway:v1"]
        new = baseline.copy()
        new["required_headers"].append("X-Extra-Header")

        result = _run_detector(baseline, new)

        assert result.returncode == 0, f"Expected PASS (exit 0), got {result.returncode}"
        assert "PASS" in result.stdout, f"Expected PASS in output, got: {result.stdout}"

    def test_fail_schema_change(self):
        """Test FAIL when JSON schema changes."""
        baseline = BASELINE_SIGNATURES["api-gateway:v1"]
        new = baseline.copy()
        new["json_schema"]["properties"]["username"]["type"] = "integer"

        result = _run_detector(baseline, new)

        assert result.returncode == 1, f"Expected FAIL (exit 1), got {result.returncode}"
        assert "FAIL" in result.stdout, f"Expected FAIL in output, got: {result.stdout}"