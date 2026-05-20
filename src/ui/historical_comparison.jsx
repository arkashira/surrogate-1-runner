import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { saveAs } from "file-saver";

/**
 * Calculate month-over-month percentage change
 * Returns null for invalid/zero previous values
 */
function calcPctChange(current, previous) {
  if (previous == null || previous === 0) return null;
  return ((current - previous) / previous) * 100;
}

/**
 * Convert data array to CSV string
 */
function dataToCsv(data) {
  const header = ["Month", "Spend", "ROI", "CTR"];
  const rows = data.map((d) => [d.month, d.spend, d.roi, d.ctr]);
  return [header, ...rows]
    .map((row) => row.map((v) => `"${v}"`).join(","))
    .join("\n");
}

/**
 * HistoricalComparison Component
 * 
 * Displays side-by-side trend graphs for spend, ROI, and CTR over the past 12 months.
 * Shows percentage change from the previous month and allows CSV export.
 * 
 * @param {string} apiEndpoint - Custom API endpoint (defaults to /api/historical_metrics?months=12)
 */
export default function HistoricalComparison({ apiEndpoint = "/api/historical_metrics?months=12" }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch data on mount
  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch(apiEndpoint);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();
        setData(json);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [apiEndpoint]);

  // Export CSV using file-saver (more reliable cross-browser)
  const handleExportCsv = () => {
    const csv = dataToCsv(data);
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    saveAs(blob, "historical_comparison.csv");
  };

  if (loading) return <div>Loading historical data…</div>;
  if (error) return <div style={{ color: "red" }}>Error: {error}</div>;
  if (!data.length) return <div>No historical data available.</div>;

  // Sort data by month (newest last)
  const sorted = [...data].sort((a, b) => a.month.localeCompare(b.month));
  const latest = sorted[sorted.length - 1];
  const previous = sorted.length > 1 ? sorted[sorted.length - 2] : null;

  // Calculate MoM changes
  const pctChanges = {
    spend: calcPctChange(latest?.spend, previous?.spend),
    roi: calcPctChange(latest?.roi, previous?.roi),
    ctr: calcPctChange(latest?.ctr, previous?.ctr),
  };

  // Reusable ChartBox component
  const ChartBox = ({ title, dataKey, color }) => (
    <div style={{ flex: 1, minWidth: 300, margin: "0 10px" }}>
      <h3>{title}</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={sorted} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey={dataKey} stroke={color} dot={false} />
        </LineChart>
      </ResponsiveContainer>
      <div style={{ marginTop: 8, fontSize: "0.9em", color: "#555" }}>
        {pctChanges[dataKey] != null ? (
          <>
            MoM change:{" "}
            <span style={{ color: pctChanges[dataKey] >= 0 ? "green" : "red" }}>
              {pctChanges[dataKey].toFixed(2)}%
            </span>
          </>
        ) : (
          "MoM change: N/A"
        )}
      </div>
    </div>
  );

  return (
    <div style={{ padding: "1rem" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <h2>Historical Campaign Comparison (Last 12 months)</h2>
        <button
          onClick={handleExportCsv}
          style={{
            padding: "8px 16px",
            backgroundColor: "#4caf50",
            color: "#fff",
            border: "none",
            borderRadius: 4,
            cursor: "pointer",
          }}
        >
          Export CSV
        </button>
      </div>
      <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
        <ChartBox title="Spend" dataKey="spend" color="#8884d8" />
        <ChartBox title="ROI" dataKey="roi" color="#82ca9d" />
        <ChartBox title="CTR (%)" dataKey="ctr" color="#ff7300" />
      </div>
    </div>
  );
}

HistoricalComparison.propTypes = {
  apiEndpoint: PropTypes.string,
};