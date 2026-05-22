import React from 'react';
import ComplianceIssues from './ComplianceIssues';

const Dashboard: React.FC = () => {
  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <ComplianceIssues />
    </div>
  );
};

export default Dashboard;