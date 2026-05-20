import React, { useState, useEffect } from 'react';

/**
 * MetricsDashboard
 *
 * Displays real‑time performance metrics collected by the firmware:
 *   • GPU bandwidth (GB/s)
 *   • Frame rate (FPS)
 *
 * Data is refreshed every 5 seconds via a GET request to `/api/metrics`.
 * The endpoint is expected to return JSON:
 *   { "gpuBandwidth": <number>, "frameRate": <number> }
 *
 * If the request fails, the component shows an error message but continues
 * attempting refreshes.
 */
export default function MetricsDashboard() {
  const [gpuBandwidth, setGpuBandwidth] = useState(null);
  const [frameRate, setFrameRate] = useState(null);
  const [error, setError] = useState(null);

  const fetchMetrics = async () => {
    try {
      const response = await fetch('/api/metrics', { cache: 'no-store' });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();
      setGpuBandwidth(data.gpuBandwidth);
      setFrameRate(data.frameRate);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch metrics:', err);
      setError('Unable to load metrics');
    }
  };

  // Initial fetch + interval refresh every 5 seconds
  useEffect(() => {
    fetchMetrics(); // immediate load
    const intervalId = setInterval(fetchMetrics, 5000);
    return () => clearInterval(intervalId); // cleanup on unmount
  }, []);

  return (
    <section className="metrics-dashboard" style={styles.container}>
      <h2 style={styles.title}>Performance Metrics</h2>

      {error && <p style={styles.error}>{error}</p>}

      <div style={styles.metricRow}>
        <span style={styles.label}>GPU Bandwidth:</span>
        <span style={styles.value}>
          {gpuBandwidth !== null ? `${gpuBandwidth} GB/s` : 'Loading…'}
        </span>
      </div>

      <div style={styles.metricRow}>
        <span style={styles.label}>Frame Rate:</span>
        <span style={styles.value}>
          {frameRate !== null ? `${frameRate} FPS` : 'Loading…'}
        </span>
      </div>
    </section>
  );
}

// Inline styles keep the component self‑contained; replace with a CSS module
// if the project prefers external styling.
const styles = {
  container: {
    padding: '1rem',
    backgroundColor: '#f9fafb',
    borderRadius: '8px',
    maxWidth: '400px',
    fontFamily: 'system-ui, sans-serif',
  },
  title: {
    marginBottom: '0.75rem',
    fontSize: '1.25rem',
    color: '#111827',
  },
  metricRow: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '0.5rem',
  },
  label: {
    fontWeight: 500,
    color: '#374151',
  },
  value: {
    fontWeight: 600,
    color: '#111827',
  },
  error: {
    color: '#b91c1c',
    marginBottom: '0.75rem',
  },
};