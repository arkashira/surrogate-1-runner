import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

/**
 * ForecastChart
 *
 * Renders a 7‑day cost forecast vs actual trend.
 * If any forecasted cost is expected to exceed the actual by more than
 * the `overageThreshold` (default 10%), an email notification is sent
 * via the `/api/notify-overage` endpoint.
 *
 * Props:
 * - data: Array<{ date: string, actual: number, forecast: number }>
 * - overageThreshold: number (percentage, e.g. 10 for 10%)
 */
const ForecastChart = ({ data, overageThreshold = 10 }) => {
  // Send email notification if overage predicted
  useEffect(() => {
    const overages = data.filter(
      (d) => d.forecast - d.actual > (overageThreshold / 100) * d.actual
    );

    if (overages.length === 0) return;

    // Prepare payload
    const payload = {
      overages: overages.map((o) => ({
        date: o.date,
        actual: o.actual,
        forecast: o.forecast,
        overage: o.forecast - o.actual,
      })),
      timestamp: new Date().toISOString(),
    };

    // POST to backend notification endpoint
    fetch('/api/notify-overage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }).catch((err) => {
      // eslint-disable-next-line no-console
      console.error('Failed to send overage notification:', err);
    });
  }, [data, overageThreshold]);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <XAxis dataKey="date" tick={{ fontSize: 12 }} />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="actual"
          stroke="#8884d8"
          name="Actual Cost"
          dot={{ r: 3 }}
          activeDot={{ r: 5 }}
        />
        <Line
          type="monotone"
          dataKey="forecast"
          stroke="#82ca9d"
          name="Forecasted Cost"
          dot={{ r: 3 }}
          activeDot={{ r: 5 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

ForecastChart.propTypes = {
  data: PropTypes.arrayOf(
    PropTypes.shape({
      date: PropTypes.string.isRequired,
      actual: PropTypes.number.isRequired,
      forecast: PropTypes.number.isRequired,
    })
  ).isRequired,
  overageThreshold: PropTypes.number,
};

export default ForecastChart;