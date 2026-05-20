import React, { useState, useEffect } from 'react';
import { useQuery } from '@apollo/client';
import { GET_COST_ANOMALIES } from '../graphql/queries';
import { CostAnomaly, CostAnomalyFilter } from '../types';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Select, MenuItem, FormControl, InputLabel, TextField, Button } from '@mui/material';

const CostAnomalyDashboard: React.FC = () => {
  const [filters, setFilters] = useState<CostAnomalyFilter>({
    severity: '',
    type: '',
    timeRange: '',
  });
  const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'ascending' | 'descending' }>({
    key: 'timestamp',
    direction: 'descending',
  });
  const { loading, error, data } = useQuery(GET_COST_ANOMALIES, {
    variables: { filters },
  });

  const handleFilterChange = (e: React.ChangeEvent<{ name?: string; value: unknown }>) => {
    const { name, value } = e.target;
    setFilters(prevFilters => ({
      ...prevFilters,
      [name as string]: value as string,
    }));
  };

  const handleSort = (key: string) => {
    let direction: 'ascending' | 'descending' = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const sortedAnomalies = React.useMemo(() => {
    if (!data?.costAnomalies) return [];
    const sortableAnomalies = [...data.costAnomalies];
    sortableAnomalies.sort((a, b) => {
      if (a[sortConfig.key] < b[sortConfig.key]) {
        return sortConfig.direction === 'ascending' ? -1 : 1;
      }
      if (a[sortConfig.key] > b[sortConfig.key]) {
        return sortConfig.direction === 'ascending' ? 1 : -1;
      }
      return 0;
    });
    return sortableAnomalies;
  }, [data, sortConfig]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <h1>Cost Anomaly Dashboard</h1>
      <div style={{ display: 'flex', gap: '16px', marginBottom: '16px' }}>
        <FormControl>
          <InputLabel>Severity</InputLabel>
          <Select
            name="severity"
            value={filters.severity}
            onChange={handleFilterChange}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="low">Low</MenuItem>
            <MenuItem value="medium">Medium</MenuItem>
            <MenuItem value="high">High</MenuItem>
          </Select>
        </FormControl>
        <FormControl>
          <InputLabel>Type</InputLabel>
          <Select
            name="type"
            value={filters.type}
            onChange={handleFilterChange}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="unexpected">Unexpected</MenuItem>
            <MenuItem value="over-budget">Over Budget</MenuItem>
          </Select>
        </FormControl>
        <TextField
          name="timeRange"
          label="Time Range"
          type="date"
          value={filters.timeRange}
          onChange={handleFilterChange}
          InputLabelProps={{ shrink: true }}
        />
      </div>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell onClick={() => handleSort('severity')}>Severity</TableCell>
              <TableCell onClick={() => handleSort('type')}>Type</TableCell>
              <TableCell onClick={() => handleSort('timestamp')}>Timestamp</TableCell>
              <TableCell onClick={() => handleSort('description')}>Description</TableCell>
              <TableCell onClick={() => handleSort('remediation')}>Remediation</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {sortedAnomalies.map((anomaly: CostAnomaly) => (
              <TableRow key={anomaly.id}>
                <TableCell>{anomaly.severity}</TableCell>
                <TableCell>{anomaly.type}</TableCell>
                <TableCell>{new Date(anomaly.timestamp).toLocaleString()}</TableCell>
                <TableCell>{anomaly.description}</TableCell>
                <TableCell>{anomaly.remediation}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default CostAnomalyDashboard;