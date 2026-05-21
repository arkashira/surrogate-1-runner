import React from 'react';
import { Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

/**
 * BenchmarkDisplay component shows a table of benchmark results.
 * Props:
 * - results: array of { metric: string; value: number; unit: string; }
 */
interface BenchmarkResult {
  metric: string;
  value: number;
  unit: string;
}

interface BenchmarkDisplayProps {
  results: BenchmarkResult[];
}

export const BenchmarkDisplay: React.FC<BenchmarkDisplayProps> = ({ results }) => {
  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h6" gutterBottom>
        Benchmark Results
      </Typography>
      <TableContainer component={Paper}>
        <Table aria-label="benchmark table">
          <TableHead>
            <TableRow>
              <TableCell>Metric</TableCell>
              <TableCell>Value</TableCell>
              <TableCell>Unit</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {results.map((r, idx) => (
              <TableRow key={idx}>
                <TableCell component="th" scope="row">
                  {r.metric}
                </TableCell>
                <TableCell>{r.value.toFixed(2)}</TableCell>
                <TableCell>{r.unit}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};