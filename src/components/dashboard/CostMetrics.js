import React from 'react';
import CostMetrics from './CostMetrics';
import CostService from '../services/costService';

const costService = new CostService();

const Dashboard = () => {
  return (
    <div>
      <CostMetrics costService={costService} />
    </div>
  );
};

export default Dashboard;