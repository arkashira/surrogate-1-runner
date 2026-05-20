import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Select, MenuItem, FormControl, InputLabel, Box } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getCostMetrics, getPolicyDecisions } from '../services/api';

interface CostMetric {
  date: string;
  cost: number;
}

interface PolicyDecision {
  id: string;
  description: string;
  status: string;
  provider: string;
  resourceType: string;
}

const CostMetricsDashboard: React.FC = () => {
  const [costMetrics, setCostMetrics] = useState<CostMetric[]>([]);
  const [policyDecisions, setPolicyDecisions] = useState<PolicyDecision[]>([]);
  const [selectedProvider, setSelectedProvider] = useState<string>('');
  const [selectedResourceType, setSelectedResourceType] = useState<string>('');

  useEffect(() => {
    const fetchData = async () => {
      const metrics = await getCostMetrics();
      const decisions = await getPolicyDecisions();
      setCostMetrics(metrics);
      setPolicyDecisions(decisions);
    };

    fetchData();
  }, []);

  const filteredPolicyDecisions = policyDecisions.filter(decision =>
    (selectedProvider === '' || decision.provider === selectedProvider) &&
    (selectedResourceType === '' || decision.resourceType === selectedResourceType)
  );

  return (
    <Box display="flex" flexDirection="column" gap={2}>
      <Box display="flex" gap={2}>
        <FormControl fullWidth>
          <InputLabel>Cloud Provider</InputLabel>
          <Select
            value={selectedProvider}
            onChange={(e) => setSelectedProvider(e.target.value)}
          >
            <MenuItem value="">All Providers</MenuItem>
            <MenuItem value="AWS">AWS</MenuItem>
            <MenuItem value="Azure">Azure</MenuItem>
            <MenuItem value="GCP">GCP</MenuItem>
          </Select>
        </FormControl>
        <FormControl fullWidth>
          <InputLabel>Resource Type</InputLabel>
          <Select
            value={selectedResourceType}
            onChange={(e) => setSelectedResourceType(e.target.value)}
          >
            <MenuItem value="">All Resource Types</MenuItem>
            <MenuItem value="Compute">Compute</MenuItem>
            <MenuItem value="Storage">Storage</MenuItem>
            <MenuItem value="Network">Network</MenuItem>
          </Select>
        </FormControl>
      </Box>
      <Box display="flex" gap={2}>
        <Card style={{ flex: 1 }}>
          <CardContent>
            <Typography variant="h5">Cost Metrics</Typography>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={costMetrics}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="cost" stroke="#8884d8" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
        <Card style={{ flex: 1 }}>
          <CardContent>
            <Typography variant="h5">Policy Decisions</Typography>
            {filteredPolicyDecisions.map(decision => (
              <Card key={decision.id} style={{ marginBottom: '10px' }}>
                <CardContent>
                  <Typography variant="h6">{decision.description}</Typography>
                  <Typography>Status: {decision.status}</Typography>
                  <Typography>Provider: {decision.provider}</Typography>
                  <Typography>Resource Type: {decision.resourceType}</Typography>
                </CardContent>
              </Card>
            ))}
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

export default CostMetricsDashboard;