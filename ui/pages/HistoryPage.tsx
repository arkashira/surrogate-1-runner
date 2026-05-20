import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Box,
  Typography,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Paper,
  TextField,
  Button,
  CircularProgress,
  Alert,
} from '@mui/material';
import { Line } from 'react-chartjs-2';
import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

Chart.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

/**
 * Validation History page
 * • Shows the last 10 validation results
 * • Displays a trend line of estimated monthly cost
 * • Allows filtering by a date range
 */
const HistoryPage: React.FC = () => {
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fromDate, setFromDate] = useState('');
  const [toDate, setToDate] = useState('');

  const fetchResults = async (from = '', to = '') => {
    setLoading(true);
    setError(null);
    try {
      const { data } = await axios.get('/api/validation/history', {
        params: { from, to, limit: 10 },
      });
      setResults(data);
    } catch (e) {
      setError('Failed to load validation history.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResults();
  }, []);

  const handleFilter = () => fetchResults(fromDate, toDate);

  // Chart data
  const chartData = {
    labels: results.map((r) => new Date(r.timestamp).toLocaleDateString()),
    datasets: [
      {
        label: 'Estimated Monthly Cost ($)',
        data: results.map((r) => r.estimatedCost),
        fill: false,
        borderColor: '#1976d2',
        tension: 0.4,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top' as const },
      title: { display: true, text: 'Estimated Monthly Cost Trend' },
    },
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Validation History
      </Typography>

      {/* Filter controls */}
      <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
        <TextField
          label="From"
          type="date"
          value={fromDate}
          onChange={(e) => setFromDate(e.target.value)}
          InputLabelProps={{ shrink: true }}
        />
        <TextField
          label="To"
          type="date"
          value={toDate}
          onChange={(e) => setToDate(e.target.value)}
          InputLabelProps={{ shrink: true }}
        />
        <Button variant="contained" onClick={handleFilter}>
          Apply
        </Button>
      </Box>

      {/* Loading / error states */}
      {loading ? (
        <CircularProgress />
      ) : error ? (
        <Alert severity="error">{error}</Alert>
      ) : (
        <>
          {/* Trend chart */}
          {results.length > 0 && (
            <Paper sx={{ mb: 3, p: 2 }}>
              <Line data={chartData} options={chartOptions} />
            </Paper>
          )}

          {/* Results table */}
          <Paper sx={{ p: 2 }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>#</TableCell>
                  <TableCell>Date</TableCell>
                  <TableCell>Result</TableCell>
                  <TableCell>Estimated Cost ($)</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {results.map((r, idx) => (
                  <TableRow key={r.id ?? idx}>
                    <TableCell>{idx + 1}</TableCell>
                    <TableCell>
                      {new Date(r.timestamp).toLocaleString(undefined, {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </TableCell>
                    <TableCell>{r.status}</TableCell>
                    <TableCell>{r.estimatedCost.toFixed(2)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Paper>
        </>
      )}
    </Box>
  );
};

export default HistoryPage;