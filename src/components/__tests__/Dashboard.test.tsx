import React from 'react';
import { render } from '@testing-library/react';
import Dashboard from '../Dashboard';

describe('Dashboard', () => {
  it('renders without crashing', () => {
    render(<Dashboard />);
  });

  it('renders the TroubleshootingGuide component', () => {
    const { getByText } = render(<Dashboard />);
    expect(getByText('CFD Simulation Troubleshooting Guide')).toBeInTheDocument();
  });
});