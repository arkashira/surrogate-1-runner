import React from 'react';
import { Container, CssBaseline, Typography } from '@mui/material';
import GPUDashboard from './components/GPUDashboard';

const App = () => {
  return (
    <Container component="main" maxWidth="md">
      <CssBaseline />
      <Typography variant="h4" component="h1" gutterBottom>
        GPU Monitoring Dashboard
      </Typography>
      <GPUDashboard />
    </Container>
  );
};

export default App;