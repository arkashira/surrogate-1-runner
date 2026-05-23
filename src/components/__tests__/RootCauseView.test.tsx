import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import RootCauseView from '../RootCauseView';
import { fetchRootCauseData } from '../../services/api';

jest.mock('../../services/api');

describe('RootCauseView', () => {
  const mockRootCauseData = [
    { resourceType: 'Compute', cost: 100, percentage: 20, resourceId: '1' },
    { resourceType: 'Storage', cost: 150, percentage: 30, resourceId: '2' },
    { resourceType: 'Network', cost: 200, percentage: 40, resourceId: '3' },
    { resourceType: 'Database', cost: 250, percentage: 50, resourceId: '4' },
    { resourceType: 'Memory', cost: 300, percentage: 60, resourceId: '5' },
  ];

  beforeEach(() => {
    (fetchRootCauseData as jest.Mock).mockResolvedValue(mockRootCauseData);
  });

  it('renders the root cause view', async () => {
    render(<RootCauseView />);

    expect(screen.getByText('Root Cause Analysis')).toBeInTheDocument();
    expect(screen.getByText('Top 5 Resources by Cost')).toBeInTheDocument();
    expect(screen.getByText('Compute')).toBeInTheDocument();
    expect(screen.getByText('Storage')).toBeInTheDocument();
    expect(screen.getByText('Network')).toBeInTheDocument();
    expect(screen.getByText('Database')).toBeInTheDocument();
    expect(screen.getByText('Memory')).toBeInTheDocument();
  });

  it('changes the time range', async () => {
    render(<RootCauseView />);

    const timeRangeSelect = screen.getByLabelText('Time Range:');
    fireEvent.change(timeRangeSelect, { target: { value: 'lastDay' } });

    expect(fetchRootCauseData).toHaveBeenCalledWith(expect.any(String), 'lastDay');
  });
});