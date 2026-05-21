import React from 'react';
import IntegrationStatus from './IntegrationStatus';

const Dashboard: React.FC = () => {
  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <IntegrationStatus />
    </div>
  );
};

export default Dashboard;