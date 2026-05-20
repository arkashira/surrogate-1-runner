import React, { useState, useEffect, useCallback } from "react";
import PropTypes from "prop-types";
import axios from "axios";

/**
 * Fetches and displays the version history for a given summary.
 * - Shows a loading spinner while the request is in flight.
 * - Displays any error that occurs.
 * - After a successful restore, it automatically refreshes the list.
 */
const VersionHistory = ({ summaryId, onRestoreSuccess }) => {
  const [versions, setVersions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // -------------------------------------------------------------------------
  // Helper: load the version list from the backend
  // -------------------------------------------------------------------------
  const loadVersions = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const { data } = await axios.get(`/api/summaries/${summaryId}/versions`);
      setVersions(data);
    } catch (err) {
      setError(err.response?.data?.message ?? err.message);
    } finally {
      setLoading(false);
    }
  }, [summaryId]);

  // -------------------------------------------------------------------------
  // Effect: run once (or when summaryId changes)
  // -------------------------------------------------------------------------
  useEffect(() => {
    loadVersions();
  }, [loadVersions]);

  // -------------------------------------------------------------------------
  // Restore a specific version
  // -------------------------------------------------------------------------
  const restoreVersion = async (versionId) => {
    if (!window.confirm("Are you sure you want to restore this version?")) return;

    try {
      await axios.post(`/api/summaries/${summaryId}/restore`, { versionId });
      alert("Version restored successfully!");
      // Refresh the version list so the UI reflects the new “current” version
      await loadVersions();
      // Notify parent (Summary) that the content may have changed
      if (onRestoreSuccess) onRestoreSuccess();
    } catch (err) {
      setError(err.response?.data?.message ?? err.message);
    }
  };

  // -------------------------------------------------------------------------
  // Render
  // -------------------------------------------------------------------------
  if (loading) return <div className="spinner">Loading version history…</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <section className="version-history">
      <h3>Version History</h3>
      {versions.length === 0 ? (
        <p>No previous versions.</p>
      ) : (
        <ul>
          {versions.map((v) => (
            <li key={v.id} className="version-item">
              <div className="meta">
                <strong>Version {v.version_number}</strong> –{" "}
                {new Date(v.created_at).toLocaleString()}
              </div>
              <pre className="content">{v.content}</pre>
              <button
                className="restore-btn"
                onClick={() => restoreVersion(v.id)}
              >
                Restore
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
};

VersionHistory.propTypes = {
  /** The ID of the summary whose versions we are displaying */
  summaryId: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  /** Optional callback fired after a successful restore – used by the parent to refresh its own data */
  onRestoreSuccess: PropTypes.func,
};

export default VersionHistory;