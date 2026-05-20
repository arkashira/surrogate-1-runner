import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import Dashboard from './dashboard';

jest.mock('axios');

describe('Dashboard', () => {
  it('fetches and displays cost data', async () => {
    const mockData = [
      { service: 'AWS', cost: 100.50, time: new Date().toISOString() },
      { service: 'GCP', cost: 200.75, time: new Date().toISOString() },
    ];

    axios.get.mockResolvedValue({ data: mockData });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText('AWS')).toBeInTheDocument();
      expect(screen.getByText('GCP')).toBeInTheDocument();
    });
  });

  it('displays loading state initially', () => {
    render(<Dashboard />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });
});