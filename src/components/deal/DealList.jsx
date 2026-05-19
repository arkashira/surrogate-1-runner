import React, { useEffect, useState, useCallback } from 'react';
import PropTypes from 'prop-types';
import './DealList.css';
import { getDeals } from '../../api/deals';

// Human‑readable mapping for the integer status stored in the DB
const STATUS_MAP = {
  0: 'In Progress',
  1: 'Closed',
  2: 'Rejected',
};

const POLL_INTERVAL_MS = 60_000; // 60 seconds

/**
 * DealList – shows a live‑updating table of deals.
 *
 * Props
 * -----
 * fetchDeals (optional) – async function returning an array of deals.
 *                         If omitted the component uses the built‑in
 *                         `getDeals` helper (axios → /api/deals).
 */
const DealList = ({ fetchDeals }) => {
  const [deals, setDeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Wrap the fetch so we can reuse it for the initial load and polling
  const loadDeals = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await (fetchDeals ? fetchDeals() : getDeals());
      setDeals(data);
    } catch (err) {
      console.error(err);
      setError(err.message ?? 'Failed to load deals');
    } finally {
      setLoading(false);
    }
  }, [fetchDeals]);

  // Initial load + polling
  useEffect(() => {
    loadDeals();
    const timer = setInterval(loadDeals, POLL_INTERVAL_MS);
    return () => clearInterval(timer);
  }, [loadDeals]);

  if (loading) return <p className="info">Loading deals…</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <table className="deal-table">
      <thead>
        <tr>
          <th>Deal ID</th>
          <th>Title</th>
          <th>Investor</th>
          <th>Status</th>
          <th>Last Updated</th>
        </tr>
      </thead>
      <tbody>
        {deals.map((deal) => {
          const statusLabel = STATUS_MAP[deal.status] ?? 'Unknown';
          const rowClass = `status-${statusLabel.replace(/\s+/g, '').toLowerCase()}`;
          const updated = new Date(deal.updated_at ?? deal.lastUpdated).toLocaleString();

          return (
            <tr key={deal.id} className={rowClass}>
              <td>{deal.id}</td>
              <td>{deal.title}</td>
              <td>{deal.investorName ?? '—'}</td>
              <td>{statusLabel}</td>
              <td>{updated}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

DealList.propTypes = {
  /** Optional custom fetcher – useful for tests or alternative data sources */
  fetchDeals: PropTypes.func,
};

DealList.defaultProps = {
  fetchDeals: null,
};

export default DealList;