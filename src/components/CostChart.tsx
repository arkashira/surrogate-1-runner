import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import './CostChart.css';

/**
 * @typedef {Object} CostRecord
 * @property {string} service
 * @property {string} region
 * @property {number} cost
 * @property {string} timestamp ISO‑8601 UTC
 */

/**
 * @typedef {Object} SeriesMap
 * @property {Array<{time: string, cost: number}>} points
 */

/**
 * Polling interval – 5 minutes
 */
const POLL_INTERVAL_MS = 5 * 60 * 1000;

/**
 * Convert raw API data into a structure that Recharts can consume.
 * @param {CostRecord[]} raw
 * @returns {{data: Array, seriesKeys: string[]}}
 */
function transformData(raw) {
  const seriesMap = new Map(); // key → array of points
  const timestampsSet = new Set();

  raw.forEach((item) => {
    const key = `${item.service} (${item.region})`;
    if (!seriesMap.has(key)) seriesMap.set(key, []);
    seriesMap.get(key).push({
      time: new Date(item.timestamp).toISOString(),
      cost: item.cost,
    });
    timestampsSet.add(item.timestamp);
  });

  const timestamps = Array.from(timestampsSet)
    .map((t) => new Date(t).toISOString())
    .sort((a, b) => new Date(a) - new Date(b));

  const data = timestamps.map((ts) => {
    const obj = { time: ts };
    seriesMap.forEach((points, key) => {
      const point = points.find((p) => p.time === ts);
      obj[key] = point ? point.cost : null;
    });
    return obj;
  });

  return { data, seriesKeys: Array.from(seriesMap.keys()) };
}

/**
 * Generates a deterministic HSL colour for a line.
 * @param {number} idx
 * @returns {string}
 */
function hueForIndex(idx) {
  const hue = (idx * 60) % 360; // 6 distinct hues
  return `hsl(${hue}, 70%, 50%)`;
}

export default function CostChart() {
  const [chartData, setChartData] = useState([]);
  const [seriesKeys, setSeriesKeys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCostData = async () => {
    try {
      const res = await fetch('/api/costs');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const raw = /** @type {CostRecord[]} */ (await res.json());
      const { data, seriesKeys } = transformData(raw);
      setChartData(data);
      setSeriesKeys(seriesKeys);
      setLoading(false);
      setError(null);
    } catch (e) {
      console.error('CostChart fetch error:', e);
      setError(e instanceof Error ? e.message : String(e));
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCostData(); // initial load
    const interval = setInterval(fetchCostData, POLL_INTERVAL_MS);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className="cost-chart-loading">Loading cost data…</div>;
  if (error) return <div className="cost-chart-error">Error: {error}</div>;

  return (
    <div className="cost-chart-container" role="img" aria-label="Real‑time cost breakdown chart">
      <h2 className="cost-chart-title">Real‑time Cost Breakdown</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart
          data={chartData}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
          <XAxis
            dataKey="time"
            tickFormatter={(t) => new Date(t).toLocaleTimeString()}
            tick={{ fontSize: 12 }}
          />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip
            labelFormatter={(label) => new Date(label).toLocaleString()}
            formatter={(value) => [`$${value.toFixed(2)}`, 'Cost']}
          />
          <Legend />
          {seriesKeys.map((key, idx) => (
            <Line
              key={key}
              type="monotone"
              dataKey={key}
              stroke={hueForIndex(idx)}
              dot={false}
              isAnimationActive={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}