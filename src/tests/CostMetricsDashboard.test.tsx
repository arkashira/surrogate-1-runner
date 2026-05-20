import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import CostMetricsDashboard from '../components/CostMetricsDashboard';
import { getCostMetrics, getPolicyDecisions } from '../services/api';

jest.mock('../services/api');

describe('CostMetricsDashboard', () => {
  beforeEach(() => {
    (getCostMetrics as jest.Mock).mockResolvedValue([
      { date: '2023-01-01', cost: 100 },
      { date: '2023-01-02', cost: 150 },
    ]);
    (getPolicyDecisions as jest.Mock).mockResolvedValue([
      { id: '1', description: 'Policy 1', status: 'Approved', provider: 'AWS', resourceType: 'Compute' },
      { id: '2', description: 'Policy 2', status: 'Pending', provider: 'Azure', resourceType: 'Storage' },
    ]);
  });

  it('renders cost metrics and policy decisions', async () => {
    render(<CostMetricsDashboard />);

    expect(await screen.findByText('Cost Metrics')).toBeInTheDocument();
    expect(await screen.findByText('Policy Decisions')).toBeInTheDocument();
  });

  it('filters policy decisions by provider and resource type', async () => {
    render(<CostMetricsDashboard />);

    fireEvent.change(screen.getByLabelText('Cloud Provider'), { target: { value: 'AWS' } });
    fireEvent.change(screen.getByLabelText('Resource Type'), { target: { value: 'Compute' } });

    expect(await screen.findByText('Policy 1')).toBeInTheDocument();
    expect(screen.queryByText('Policy 2')).not.toBeInTheDocument();
  });
});