import React from 'react';
import useCredits from '../hooks/useCredits';

const Dashboard = () => {
  const { credits, loading } = useCredits();   // default 60 s refresh

  if (loading) {
    return <div>Loading credit information…</div>;
  }

  if (!credits) {
    return <div style={{ color: 'red' }}>Failed to load credits.</div>;
  }

  const { monthly, bulk } = credits;

  const monthlyPct = monthly.total ? (monthly.used / monthly.total) * 100 : 0;
  const bulkPct    = bulk.total    ? (bulk.used    / bulk.total)    * 100 : 0;

  const bulkLow = bulk.total && (bulk.remaining / bulk.total) < 0.2;

  const barStyle = (pct, warning) => ({
    width: `${pct}%`,
    backgroundColor: warning ? 'red' : pct < 50 ? 'green' : 'orange',
    height: '1rem',
    transition: 'width 0.3s ease',
  });

  return (
    <section style={{ padding: '1rem', maxWidth: '600px' }}>
      <h1>Credit Dashboard</h1>

      {/* Monthly Credits */}
      <div style={{ marginBottom: '1.5rem' }}>
        <h2>Monthly Credits</h2>
        <div style={{ background: '#eee', borderRadius: '4px' }}>
          <div style={barStyle(monthlyPct, false)} />
        </div>
        <p>
          {monthly.used} / {monthly.total} ({monthlyPct.toFixed(1)} %)
        </p>
      </div>

      {/* Bulk Credits */}
      <div>
        <h2>Bulk Credits</h2>
        <div style={{ background: '#eee', borderRadius: '4px' }}>
          <div style={barStyle(bulkPct, bulkLow)} />
        </div>
        <p>
          {bulk.used} / {bulk.total} ({bulkPct.toFixed(1)} %)
        </p>
        {bulkLow && (
          <p style={{ color: 'red', fontWeight: 'bold' }}>
            ⚠️ Low bulk‑credit warning! (< 20 % remaining)
          </p>
        )}
      </div>
    </section>
  );
};

export default Dashboard;