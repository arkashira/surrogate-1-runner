import React, { useEffect, useState, useCallback } from "react";

/**
 * Fetch compliance data from the backend.
 * Expected response shape:
 * [
 *   {
 *     model: string,
 *     status: "compliant" | "non‑compliant" | "unknown",
 *     rule: string,
 *     violations: string[],   // list of violation messages
 *     timestamp: string       // ISO‑8601 datetime
 *   },
 *   ...
 * ]
 */
async function fetchComplianceData() {
  const response = await fetch("/api/compliance");
  if (!response.ok) {
    throw new Error(`Failed to fetch compliance data: ${response.status}`);
  }
  return response.json();
}

/**
 * ComplianceDashboard
 *
 * Shows a table of model compliance information with filtering controls.
 * Auto‑refreshes every 10 minutes.
 */
export default function ComplianceDashboard() {
  const [rawData, setRawData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filter state
  const [ruleFilter, setRuleFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [dateFilter, setDateFilter] = useState("");

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchComplianceData();
      setRawData(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial load + auto‑refresh every 10 minutes
  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 10 * 60 * 1000); // 10 min
    return () => clearInterval(interval);
  }, [loadData]);

  // Derive filtered data
  const filteredData = rawData.filter((row) => {
    const matchesRule = ruleFilter ? row.rule === ruleFilter : true;
    const matchesStatus = statusFilter ? row.status === statusFilter : true;
    const matchesDate = dateFilter
      ? new Date(row.timestamp).toISOString().slice(0, 10) === dateFilter
      : true;
    return matchesRule && matchesStatus && matchesDate;
  });

  // Unique values for filter dropdowns
  const uniqueRules = Array.from(new Set(rawData.map((r) => r.rule))).sort();
  const uniqueStatuses = Array.from(
    new Set(rawData.map((r) => r.status))
  ).sort();

  return (
    <div className="compliance-dashboard">
      <h2>Compliance Dashboard</h2>

      {error && <div className="error">Error: {error}</div>}

      <div className="filters" style={{ marginBottom: "1rem" }}>
        <label>
          Rule:
          <select
            data-testid="rule-filter"
            value={ruleFilter}
            onChange={(e) => setRuleFilter(e.target.value)}
          >
            <option value="">All</option>
            {uniqueRules.map((rule) => (
              <option key={rule} value={rule}>
                {rule}
              </option>
            ))}
          </select>
        </label>

        <label style={{ marginLeft: "1rem" }}>
          Status:
          <select
            data-testid="status-filter"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="">All</option>
            {uniqueStatuses.map((status) => (
              <option key={status} value={status}>
                {status}
              </option>
            ))}
          </select>
        </label>

        <label style={{ marginLeft: "1rem" }}>
          Ingestion Date:
          <input
            data-testid="date-filter"
            type="date"
            value={dateFilter}
            onChange={(e) => setDateFilter(e.target.value)}
          />
        </label>
      </div>

      {loading ? (
        <div data-testid="loading">Loading…</div>
      ) : (
        <table data-testid="compliance-table" className="table">
          <thead>
            <tr>
              <th>Model</th>
              <th>Status</th>
              <th>Rule</th>
              <th>Violations</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {filteredData.length === 0 ? (
              <tr>
                <td colSpan={5}>No records match the selected filters.</td>
              </tr>
            ) : (
              filteredData.map((row, idx) => (
                <tr key={idx}>
                  <td>{row.model}</td>
                  <td>{row.status}</td>
                  <td>{row.rule}</td>
                  <td>
                    {row.violations && row.violations.length > 0
                      ? row.violations.join("; ")
                      : "None"}
                  </td>
                  <td>{new Date(row.timestamp).toLocaleString()}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}