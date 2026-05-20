import React, { useEffect, useState, useRef } from "react";
import { getDrifts } from "../api/drifts";
import "./DriftTable.css";

/**
 * DriftTable – shows recent drift events in a table.
 *
 * Features:
 *   • fetches on mount + refreshes every 60 s,
 *   • displays loading, error, and empty states,
 *   • avoids state updates after unmount,
 *   • tolerates missing fields (shows “‑” placeholder).
 */
export default function DriftTable() {
  const [drifts, setDrifts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const mounted = useRef(true);               // tracks component mount status

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getDrifts();
      if (mounted.current) setDrifts(data);
    } catch (err) {
      console.error("Failed to load drifts:", err);
      if (mounted.current) setError("Unable to load drift events.");
    } finally {
      if (mounted.current) setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();                     // initial load
    const interval = setInterval(fetchData, 60_000); // refresh each minute
    return () => {
      mounted.current = false;      // prevent state updates after unmount
      clearInterval(interval);
    };
  }, []);

  // ----- UI -----------------------------------------------------------------
  if (loading) {
    return <div className="drift-table--status">Loading drift events…</div>;
  }

  if (error) {
    return <div className="drift-table--status error">{error}</div>;
  }

  if (drifts.length === 0) {
    return <div className="drift-table--status">No recent drift events.</div>;
  }

  return (
    <div className="drift-table-wrapper">
      <table className="drift-table">
        <thead>
          <tr>
            <th>Service</th>
            <th>Deployment</th>
            <th>Timestamp</th>
            <th>Diff</th>
          </tr>
        </thead>
        <tbody>
          {drifts.map((d, idx) => (
            <tr key={idx}>
              <td>{d.service ?? "‑"}</td>
              <td>{d.deployment ?? "‑"}</td>
              <td>
                {d.timestamp
                  ? new Date(d.timestamp).toLocaleString()
                  : "‑"}
              </td>
              <td>
                <pre className="drift-table__diff">{d.diff ?? ""}</pre>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}