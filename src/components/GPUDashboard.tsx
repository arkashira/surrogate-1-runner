import React, { useEffect, useState } from 'react';
import { Card, CardContent, Typography, Grid, CircularProgress } from '@mui/material';
import { getGPUPerformance, getFirmwareStatus } from '../services/gpuService';

const GPUDashboard = () => {
  const [gpuPerformance, setGPUPerformance] = useState(null);
  const [firmwareStatus, setFirmwareStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const performanceData = await getGPUPerformance();
        const firmwareData = await getFirmwareStatus();
        setGPUPerformance(performanceData);
        setFirmwareStatus(firmwareData);
      } catch (error) {
        console.error('Error fetching GPU data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000); // Refresh every 5 seconds

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h5" component="h2">
              GPU Performance
            </Typography>
            {gpuPerformance && (
              <div>
                <Typography color="textSecondary">
                  Usage: {gpuPerformance.usage}%
                </Typography>
                <Typography color="textSecondary">
                  Temperature: {gpuPerformance.temperature}°C
                </Typography>
                <Typography color="textSecondary">
                  Memory Usage: {gpuPerformance.memoryUsage} MB
                </Typography>
              </div>
            )}
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h5" component="h2">
              Firmware Status
            </Typography>
            {firmwareStatus && (
              <div>
                <Typography color="textSecondary">
                  Version: {firmwareStatus.version}
                </Typography>
                <Typography color="textSecondary">
                  Status: {firmwareStatus.status}
                </Typography>
                <Typography color="textSecondary">
                  Last Updated: {new Date(firmwareStatus.lastUpdated).toLocaleString()}
                </Typography>
              </div>
            )}
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default GPUDashboard;