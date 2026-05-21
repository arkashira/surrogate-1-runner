import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { fetchCostMetrics } from '../services/costinelApi';

interface CostMetric {
  timestamp: string;
  cost: number;
}

interface CostMetricsWidgetProps {
  serviceTypes: string[];
  initialServiceType?: string;
  initialTimeRange?: string;
}

const CostMetricsWidget: React.FC<CostMetricsWidgetProps> = ({ serviceTypes, initialServiceType = 'all', initialTimeRange = '24h' }) => {
  const [costData, setCostData] = useState<CostMetric[]>([]);
  const [selectedService, setSelectedService] = useState<string>(initialServiceType);
  const [timeRange, setTimeRange] = useState<string>(initialTimeRange);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const data = await fetchCostMetrics(selectedService, timeRange);
        setCostData(data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch cost metrics');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 300000); // Update every 5 minutes

    return () => clearInterval(intervalId);
  }, [selectedService, timeRange]);

  const handleServiceChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setSelectedService(event.target.value as string);
  };

  const handleTimeRangeChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setTimeRange(event.target.value as string);
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="h2">
          Cost Metrics
        </Typography>
        <FormControl fullWidth>
          <InputLabel>Service Type</InputLabel>
          <Select value={selectedService} onChange={handleServiceChange}>
            {serviceTypes.map((type) => (
              <MenuItem key={type} value={type}>{type}</MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl fullWidth>
          <InputLabel>Time Range</InputLabel>
          <Select value={timeRange} onChange={handleTimeRangeChange}>
            <MenuItem value="24h">Last 24 Hours</MenuItem>
            <MenuItem value="7d">Last 7 Days</MenuItem>
            <MenuItem value="30d">Last 30 Days</MenuItem>
          </Select>
        </FormControl>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={costData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="timestamp" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="cost" stroke="#8884d8" activeDot={{ r: 8 }} />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};

export default CostMetricsWidget;