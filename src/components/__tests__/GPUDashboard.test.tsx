import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import GPUDashboard from '../GPUDashboard';
import { getGPUPerformance, getFirmwareStatus } from '../../services/gpuService';

jest.mock('../../services/gpuService');

describe('GPUDashboard', () => {
  beforeEach(() => {
    (getGPUPerformance as jest.Mock).mockResolvedValue({
      usage: 75,
      temperature: 65,
      memoryUsage: 4096,
    });
    (getFirmwareStatus as jest.Mock).mockResolvedValue({
      version: '1.0.0',
      status: 'Up to date',
      lastUpdated: '2023-05-04T12:00:00Z',
    });
  });

  it('renders loading state initially', () => {
    render(<GPUDashboard />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('renders GPU performance data after loading', async () => {
    render(<GPUDashboard />);
    await waitFor(() => {
      expect(screen.getByText('GPU Performance')).toBeInTheDocument();
      expect(screen.getByText('Usage: 75%')).toBeInTheDocument();
      expect(screen.getByText('Temperature: 65°C')).toBeInTheDocument();
      expect(screen.getByText('Memory Usage: 4096 MB')).toBeInTheDocument();
    });
  });

  it('renders firmware status data after loading', async () => {
    render(<GPUDashboard />);
    await waitFor(() => {
      expect(screen.getByText('Firmware Status')).toBeInTheDocument();
      expect(screen.getByText('Version: 1.0.0')).toBeInTheDocument();
      expect(screen.getByText('Status: Up to date')).toBeInTheDocument();
      expect(screen.getByText('Last Updated:')).toBeInTheDocument();
    });
  });
});