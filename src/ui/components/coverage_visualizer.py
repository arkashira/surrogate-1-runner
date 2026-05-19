"""
Coverage visualizer module.

This module provides a simple API to generate an HTML coverage report
that highlights uncovered lines in source files.  It is intentionally
light‑weight to keep report generation under the 5 s threshold for
medium‑sized projects.

The module expects coverage data in the following format: