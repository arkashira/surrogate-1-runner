import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import DashboardLayout from './DashboardLayout';

describe('DashboardLayout', () => {
  it('renders summary cards', () => {
    const { getByText } = render(<DashboardLayout />);
    expect(getByText('Active Alerts')).toBeInTheDocument();
    expect(getByText('System Status')).toBeInTheDocument();
    expect(getByText('Last Updated')).toBeInTheDocument();
  });

  it('renders sidebar navigation', () => {
    const { getByText } = render(<DashboardLayout />);
    expect(getByText('Dashboard')).toBeInTheDocument();
    expect(getByText('Alerts')).toBeInTheDocument();
    expect(getByText('Metrics')).toBeInTheDocument();
    expect(getByText('Settings')).toBeInTheDocument();
  });
});