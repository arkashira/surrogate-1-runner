import React, { useEffect, useState } from "react";

/**
 * CostDashboard
 *
 * Displays unified cloud spend across AWS, GCP, and Azure.
 * Allows the user to select a custom time range (last 7, 30, or 90 days).
 *
 * Expected API contract (GET /api/cost?days=<N>):
 * {
 *   "providers": [
 *     {
 *       "name": "AWS",
 *       "total": 1234.56,
 *       "breakdown": [
 *         { "service": "EC2", "cost": 800 },
 *         { "service": "S3", "cost": 200 },
 *         ...
 *       ]
 *     },
 *     { "name": "GCP", ... },
 *     { "name": "Azure", ... }
 *   ]
 * }
 */
export default function CostDashboard() {
  const TIME_RANGES = [
    { label: "Last 7 days", value: 7 },
    { label: "Last 30 days", value: 30 },
    { label: "Last 90 days", value: 90 },
  ];

  const [selectedDays, setSelectedDays] = useState(TIME_RANGES[0].value);
  const [providersData, setProvidersData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchCostData = async (days) => {
    setLoading(true);
    setError(null);
    try {
      const resp = await fetch(`/api/cost?days=${days}`);
      if (!resp.ok) {
        throw new Error(`API error: ${resp.status}`);
      }
      const json = await resp.json();
      setProvidersData(json.providers || []);
    } catch (e) {
      setError(e.message);
      setProvidersData([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCostData(selectedDays);
  }, [selectedDays]);

  const handleRangeChange = (e) => {
    setSelectedDays(parseInt(e.target.value, 10));
  };

  return (
    <div className="cost-dashboard" style={{ padding: "1rem", fontFamily: "Arial, sans-serif" }}>
      <h2>Cloud Spend Dashboard</h2>

      <div style={{ marginBottom: "1rem" }}>
        <label htmlFor="time-range-select" style={{ marginRight: "0.5rem" }}>
          Time range:
        </label>
        <select id="time-range-select" value={selectedDays} onChange={handleRangeChange}>
          {TIME_RANGES.map((tr) => (
            <option key={tr.value} value={tr.value}>
              {tr.label}
            </option>
          ))}
        </select>
      </div>

      {loading && <p>Loading cost data...</p>}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {!loading && !error && providersData.length === 0 && <p>No cost data available.</p>}

      {!loading && !error && providersData.length > 0 && (
        <div className="providers">
          {providersData.map((provider) => (
            <section key={provider.name} style={{ marginBottom: "2rem" }}>
              <h3>{provider.name}</h3>
              <p>
                <strong>Total Spend:</strong> ${provider.total.toFixed(2)}
              </p>

              {provider.breakdown && provider.breakdown.length > 0 ? (
                <table
                  style={{
                    width: "100%",
                    borderCollapse: "collapse",
                    marginTop: "0.5rem",
                  }}
                >
                  <thead>
                    <tr>
                      <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>
                        Service / Resource
                      </th>
                      <th style={{ borderBottom: "1px solid #ddd", textAlign: "right" }}>
                        Cost (USD)
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {provider.breakdown.map((item, idx) => (
                      <tr key={idx}>
                        <td style={{ padding: "0.25rem 0" }}>{item.service}</td>
                        <td style={{ padding: "0.25rem 0", textAlign: "right" }}>
                          ${item.cost.toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <p>No breakdown data.</p>
              )}
            </section>
          ))}
        </div>
      )}
    </div>
  );
}