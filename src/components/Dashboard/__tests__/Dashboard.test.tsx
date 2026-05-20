import React from 'react';
import { render, screen } from '@testing-library/react';
import Dashboard from '../Dashboard';

describe('Dashboard', () => {
  it('renders the dashboard with the free tier limitations section', () => {
    render(<Dashboard />);
    expect(screen.getByText('Free Tier Limitations')).toBeInTheDocument();
  });
});