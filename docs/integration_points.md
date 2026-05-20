
## Integration Points for Test Filtering & Coverage Reporting

This document outlines how the new test filtering and coverage reporting features integrate with the existing surrogate‑1 workflow and test ecosystem.

| Feature | Integration Point | How it Works | Performance Impact |
|---------|-------------------|--------------|--------------------|
| **Test Filtering** | GitHub Actions `workflow_dispatch` input `filter` | Users can trigger the `Test Filter & Coverage` workflow manually and supply a pytest `-k` style filter string. The workflow passes this string to the test runner via the `TEST_FILTER` environment variable. | Minimal. Only the selected tests are executed, reducing runtime proportionally to the filter. |
| **Coverage Reporting** | `pytest-cov` plugin | The workflow runs `pytest` with `--cov=src` and generates an XML coverage report (`coverage.xml`). The report is uploaded as an artifact for later inspection or integration with external coverage services. | Overhead is limited to the coverage collection step; typical increase < 5 % for most test suites. |
| **Compatibility with Existing Frameworks** | Existing `pytest` tests | No changes are required to the test code. The workflow simply adds the `--cov` flag. If a project uses a different test runner (e.g., `unittest`), the workflow can be extended to detect and run the appropriate command. | No impact on existing tests. |
| **Workflow Integration** | `.github/workflows/ci.yml` | The new workflow is independent and can coexist with the existing CI pipeline. It can be triggered automatically on pushes/PRs or manually via the UI. | No interference with existing jobs; runs as a separate job. |
| **Documentation** | `docs/integration_points.md` | Updated to reflect the new workflow, inputs, and usage examples. | N/A |

### Usage Examples

1. **Run all tests with coverage**