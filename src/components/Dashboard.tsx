import React from 'react';
import { Grid, Paper } from '@mui/material';
import TroubleshootingGuide from './TroubleshootingGuide';

const Dashboard = () => {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Paper>
          <TroubleshootingGuide />
        </Paper>
      </Grid>
    </Grid>
  );
};

export default Dashboard;