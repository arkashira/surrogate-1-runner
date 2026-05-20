import React, { useState, useEffect, useCallback } from 'react';
import { fetchAuditItems, fetchCommitDiff } from '../api';
import './AuditList.css';

const COLUMNS = [
  { key: 'id', label: 'ID', width: '80px' },
  { key: 'score', label: 'Score', width: '80px' },
  { key: 'policy', label: 'Policy', width: '200px' },
  { key: 'commitSha', label: 'Commit SHA', width: '120px' },
  { key: 'businessImpact', label: 'Business Impact', width: 'auto' },
];

const REFRESH_INTERVAL_MS = 30000;

function DiffModal({ commitSha, diff, isLoading, onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Commit: {commitSha?.substring(0, 7)}</h3>
          <button className="close-btn" onClick={onClose} aria-label="Close">
            ×
          </button>
        </div>
        <div className="modal-body">
          {isLoading ? (
            <div className="diff-loading">Loading diff...</div>
          ) : (
            <pre className="diff-content">{diff}</pre>
          )}
        </div>
      </div>
    </div>
  );
}

export default function AuditList() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedItem, setSelectedItem] = useState(null);
  const [diff, setDiff] = useState(null);
  const [diffLoading, setDiffLoading] = useState(false);

  const loadData = useCallback(async () => {
    try {
      const data = await fetchAuditItems();
      setItems(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial load + auto-refresh
  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, REFRESH_INTERVAL_MS);
    return () => clearInterval(interval);
  }, [loadData]);

  // Fetch diff when item selected
  useEffect(() => {
    if (!selectedItem) return;
    
    let cancelled = false;
    setDiffLoading(true);
    setDiff(null);

    fetchCommitDiff(selectedItem.commitSha)
      .then((data) => {
        if (!cancelled) setDiff(data);
      })
      .catch((err) => {
        if (!cancelled) setDiff(`Error: ${err.message}`);
      })
      .finally(() => {
        if (!cancelled) setDiffLoading(false);
      });

    return () => { cancelled = true; };
  }, [selectedItem?.commitSha]);

  const handleClose = () => {
    setSelectedItem(null);
    setDiff(null);
  };

  if (loading && !items.length) {
    return <div className="audit-loading">Loading audit items...</div>;
  }

  if (error && !items.length) {
    return <div className="audit-error">Error: {error}</div>;
  }

  return (
    <div className="audit-container">
      <header className="audit-header">
        <h2>Audit Findings Dashboard</h2>
        <span className="refresh-badge">Auto-refresh: 30s</span>
      </header>

      <div className="table-wrapper">
        <table className="audit-table">
          <thead>
            <tr>
              {COLUMNS.map((col) => (
                <th key={col.key} style={{ width: col.width }}>{col.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr
                key={item.id}
                onClick={() => setSelectedItem(item)}
                className={selectedItem?.id === item.id ? 'selected' : ''}
              >
                <td>{item.id}</td>
                <td><span className="score-badge">{item.score}</span></td>
                <td>{item.policy}</td>
                <td className="sha">{item.commitSha?.substring(0, 7)}</td>
                <td>{item.businessImpact}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedItem && (
        <DiffModal
          commitSha={selectedItem.commitSha}
          diff={diff}
          isLoading={diffLoading}
          onClose={handleClose}
        />
      )}
    </div>
  );
}