import React from 'react';
import { render, screen } from '@testing-library/react';
import IntegrationStatus from '../../../components/Dashboard/IntegrationStatus';
import { useIntegrationStatus } from '../../../hooks/useIntegrationStatus';

jest.mock('../../../hooks/useIntegrationStatus');

describe('IntegrationStatus', () => {
  it('renders loading state', () => {
    (useIntegrationStatus as jest.Mock).mockReturnValue({ status: 'loading', error: null });
    render(<IntegrationStatus />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders error state', () => {
    (useIntegrationStatus as jest.Mock).mockReturnValue({ status: 'error', error: new Error('Failed to fetch') });
    render(<IntegrationStatus />);
    expect(screen.getByText('Error: Failed to fetch')).toBeInTheDocument();
  });

  it('renders integration status', () => {
    (useIntegrationStatus as jest.Mock).mockReturnValue({ status: 'connected', error: null });
    render(<IntegrationStatus />);
    expect(screen.getByText('Status: connected')).toBeInTheDocument();
  });
});