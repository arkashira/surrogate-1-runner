import promClient from 'prom-client';

// Create a Registry to register the metrics
export const register = new promClient.Registry();

// Add default metrics (CPU, memory, etc.)
promClient.collectDefaultMetrics({ register };

// 1. Counter: Total number of messages sent
export const messageSentCounter = new promClient.Counter({
  name: 'messages_sent_total',
  help: 'Total number of messages sent',
  registers: [register],
});

// 2. Counter: Total number of panel opens
export const panelOpenCounter = new promClient.Counter({
  name: 'panel_open_total',
  help: 'Total number of times a panel was opened',
  registers: [register],
});

// 3. Histogram: Duration of panel sessions (in seconds)
// Histograms are better than Gauges for tracking latency distribution (p50, p95, p99)
export const panelSessionDuration = new promClient.Histogram({
  name: 'panel_session_duration_seconds',
  help: 'Duration of panel sessions in seconds',
  buckets: [0.1, 0.5, 1, 2, 5, 10, 30], // Buckets for latency tracking
  registers: [register],
});