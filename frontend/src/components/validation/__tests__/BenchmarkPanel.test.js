import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import BenchmarkPanel from '../BenchmarkPanel';

test('renders benchmarks correctly', async () => {
  const metricDefinition = {}; // Mock metric definition if needed
  render(<BenchmarkPanel metricDefinition={metricDefinition} />);

  expect(screen.getByText('Benchmarks')).toBeInTheDocument();

  // Simulate selecting an industry and stage
  fireEvent.change(screen.getByLabelText(/Select Industry/i), { target: { value: 'SaaS' } });
  fireEvent.change(screen.getByLabelText(/Select Stage/i), { target: { value: 'pre-seed' } });

  // Wait for benchmarks to load and check if they are displayed
  await waitFor(() => {
    expect(screen.getByText(/Median:/i)).toBeInTheDocument();
    expect(screen.getByText(/25th Percentile:/i)).toBeInTheDocument();
    expect(screen.getByText(/75th Percentile:/i)).toBeInTheDocument();
  });
});