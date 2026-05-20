import React from 'react';
import Sidebar from './Sidebar';
import SummaryCards from './SummaryCards';

const DashboardLayout = () => {
  return (
    <div className="dashboard-layout">
      <Sidebar />
      <div className="dashboard-content">
        <SummaryCards />
      </div>
    </div>
  );
};

export default DashboardLayout;