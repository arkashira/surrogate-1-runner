// ... (existing code)

// Export buttons
<div className="dashboard__actions">
  <button
    className="btn btn--secondary"
    onClick={refresh}
    disabled={loading}
  >
    {loading ? 'Refreshing...' : 'Refresh Now'}
  </button>
  <button className="btn btn--primary" onClick={handleExportCSV}>
    Export CSV
  </button>
  <button className="btn btn--secondary" onClick={handleExportJSON}>
    Export JSON
  </button>
</div>

// Export handlers
const handleExportCSV = () => exportReport('csv');
const handleExportJSON = () => exportReport('json');

// ... (remaining code)