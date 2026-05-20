import React from 'react';

const SummaryCards = () => {
  return (
    <div className="summary-cards">
      <div className="card">
        <h2>Active Alerts</h2>
        <p>0</p>
      </div>
      <div className="card">
        <h2>System Status</h2>
        <p>Healthy</p>
      </div>
      <div className="card">
        <h2>Last Updated</h2>
        <p>Just now</p>
      </div>
    </div>
  );
};

export default SummaryCards;