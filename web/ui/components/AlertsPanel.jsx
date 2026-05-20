import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";

/**
 * AlertsPanel
 *
 * Fetches real‑time cost anomaly alerts from the backend and displays them.
 * The component polls the `/api/alerts` endpoint every 60 seconds to keep the UI
 * up‑to‑date (alerts are emitted by the backend within 5 minutes of detection).
 *
 * Expected alert payload shape:
 *   {
 *     id: string,
 *     message: string,
 *     timestamp: ISO8601 string,
 *     rootCause?: string   // optional suggestion from the backend
 *   }
 */
export default function AlertsPanel({ pollIntervalMs = 60000 }) {
  const [alerts, setAlerts] = useState([]);
  const [error, setError] = useState(null);

  const fetchAlerts = async () => {
    try {
      const resp = await fetch("/api/alerts", {
        headers: {
          "Accept": "application/json",
        },
        cache: "no-store",
      });
      if (!resp.ok) {
        throw new Error(`HTTP ${resp.status}`);
      }
      const data = await resp.json();
      // Ensure alerts are sorted newest‑first
      const sorted = data.sort(
        (a, b) => new Date(b.timestamp) - new Date(a.timestamp)
      );
      setAlerts(sorted);
      setError(null);
    } catch (e) {
      console.error("Failed to fetch alerts:", e);
      setError(e.message);
    }
  };

  // Initial load + periodic polling
  useEffect(() => {
    fetchAlerts(); // initial
    const timer = setInterval(fetchAlerts, pollIntervalMs);
    return () => clearInterval(timer);
  }, [pollIntervalMs]);

  const formatTimestamp = (ts) => {
    const d = new Date(ts);
    return d.toLocaleString(undefined, {
      hour12: false,
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  return (
    <div className="alerts-panel">
      <h2>Cost Anomaly Alerts</h2>
      {error && (
        <div className="alerts-error" role="alert">
          Unable to load alerts: {error}
        </div>
      )}
      {alerts.length === 0 && !error && (
        <div className="alerts-empty">No active anomalies.</div>
      )}
      <ul className="alerts-list">
        {alerts.map((alert) => (
          <li key={alert.id} className="alert-item">
            <div className="alert-message">{alert.message}</div>
            <div className="alert-meta">
              <span className="alert-timestamp">
                {formatTimestamp(alert.timestamp)}
              </span>
              {alert.rootCause && (
                <span className="alert-rootcause">
                  Suggested root cause: {alert.rootCause}
                </span>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

AlertsPanel.propTypes = {
  /** Polling interval in milliseconds; defaults to 60 seconds */
  pollIntervalMs: PropTypes.number,
};