import React from 'react';
import { Grid } from '@mui/material';
import CostMetricsWidget from './CostMetricsWidget';

const Dashboard: React.FC = () => {
  const serviceTypes = ['all', 'compute', 'storage', 'network'];

  return (
    <div>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <CostMetricsWidget serviceTypes={serviceTypes} />
        </Grid>
      </Grid>
    </div>
  );
};

export default Dashboard;