import React from 'react';
import { Grid } from '@mui/material';
import FreeTierLimitations from './FreeTierLimitations';

const Dashboard: React.FC = () => {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <FreeTierLimitations />
      </Grid>
      {/* Other dashboard components */}
    </Grid>
  );
};

export default Dashboard;