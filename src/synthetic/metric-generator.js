/**
 * Synthetic metric generator – JavaScript version
 *
 * Guarantees:
 *   • ≥ minCount metrics (default 100)
 *   • Types: gauge | count | distribution
 *   • Monotonic timestamps inside a 1‑minute window
 *   • Distribution values are arrays of 5‑10 numbers
 *
 * Export: generateMetrics({ minCount?, timeWindowMs? })
 */

const METRIC_TYPES = ['gauge', 'count', 'distribution'];
const PREFIXES = ['cpu', 'memory', 'disk', 'network', 'request', 'error', 'latency'];
const SUFFIXES = ['utilization', 'usage', 'throughput', 'duration', 'rate', 'count'];

/* ---------- helpers ---------- */
function randomMetricName() {
  const p = PREFIXES[Math.floor(Math.random() * PREFIXES.length)];
  const s = SUFFIXES[Math.floor(Math.random() * SUFFIXES.length)];
  return `metric.${p}.${s}`;
}

function randomValue(type) {
  switch (type) {
    case 'gauge':
      return Number((Math.random() * 100).toFixed(2));
    case 'count':
      return Math.floor(Math.random() * 1000);
    case 'distribution': {
      const len = 5 + Math.floor(Math.random() * 6); // 5‑10
      const arr = Array.from({ length: len }, () =>
        Number((Math.random() * 200).toFixed(2))
      );
      return arr;
    }
    default:
      return null;
  }
}

/* ---------- main generator ---------- */
function generateMetrics({ minCount = 100, timeWindowMs = 60000 } = {}) {
  const count = Math.max(minCount, 100);
  const now = Date.now();
  const start = now - timeWindowMs;
  const interval = timeWindowMs / count;

  const metrics = [];

  for (let i = 0; i < count; i++) {
    const type = METRIC_TYPES[Math.floor(Math.random() * METRIC_TYPES.length)];
    // Small jitter (±5 ms) keeps timestamps monotonic but not perfectly uniform.
    const jitter = Math.floor(Math.random() * 11) - 5;
    const ts = Math.round(start + i * interval + jitter);

    metrics.push({
      name: randomMetricName(),
      type,
      timestamp: ts,
      value: randomValue(type),
    });
  }

  // Already monotonic; no need to sort.
  return metrics;
}

/* ---------- optional CLI for manual testing ---------- */
if (require.main === module) {
  const metrics = generateMetrics({ minCount: 120 });
  console.log(JSON.stringify(metrics, null, 2));
}

module.exports = { generateMetrics };