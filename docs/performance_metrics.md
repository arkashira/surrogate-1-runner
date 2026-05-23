# Performance Metrics Documentation

## Overview

This document defines the performance benchmarks and metrics for the surrogate-1 parser pipeline. All metrics are measured under production-like conditions with the parallel ingest workers.

## Performance Benchmarks

### Data Stream Processing

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Throughput (small schema) | ≥ 500 KB/s per worker | `time python -m surrogate.parser --schema small --input /dev/stdin` |
| Throughput (large schema) | ≥ 200 KB/s per worker | `time python -m surrogate.parser --schema large --input /dev/stdin` |
| Latency (p99) | ≤ 50ms per record | Distributed tracing with OpenTelemetry |
| Memory footprint | ≤ 256 MB per worker | `top -p <pid> -o %MEM` |
| CPU utilization | ≤ 75% per core | `mpstat -P ALL 1` |

### Stability Under Load

| Condition | Duration | Expected Failures |
|-----------|----------|-------------------|
| Sustained 16 parallel workers | 4 hours | 0 |
| Memory pressure (swap active) | 2 hours | 0 |
| Network latency spikes (200ms) | 30 minutes | 0 |
| Disk I/O saturation | 1 hour | 0 |

## Benchmark Test Suite

### Test 1: Large Dataset Stream