import React from 'react';
import { render, screen } from '@testing-library/react';
import Dashboard from '../../../components/Dashboard/Dashboard';

jest.mock('../../../components/Dashboard/IntegrationStatus', () => () => <div>IntegrationStatus</div>);

describe('Dashboard', () => {
  it('renders Dashboard component', () => {
    render(<Dashboard />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('IntegrationStatus')).toBeInTheDocument();
  });
});