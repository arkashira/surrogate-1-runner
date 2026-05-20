import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import Dashboard from '../Dashboard';

jest.mock('axios');

describe('Dashboard', () => {
  it('renders loading state initially', () => {
    axios.get.mockImplementationOnce(() =>
      new Promise(() => {})
    );

    render(<Dashboard />);

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('displays cost data after loading', async () => {
    const mockData = [
      {
        id: 1,
        provider: 'AWS',
        resourceType: 'EC2',
        cost: '$100',
        team: 'team1',
        project: 'project1',
      },
      {
        id: 2,
        provider: 'Azure',
        resourceType: 'VM',
        cost: '$200',
        team: 'team2',
        project: 'project2',
      },
    ];

    axios.get.mockResolvedValueOnce({ data: mockData });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText('AWS')).toBeInTheDocument();
      expect(screen.getByText('Azure')).toBeInTheDocument();
    });
  });

  it('filters data based on selected filter', async () => {
    const mockData = [
      {
        id: 1,
        provider: 'AWS',
        resourceType: 'EC2',
        cost: '$100',
        team: 'team1',
        project: 'project1',
      },
      {
        id: 2,
        provider: 'Azure',
        resourceType: 'VM',
        cost: '$200',
        team: 'team2',
        project: 'project2',
      },
    ];

    axios.get.mockResolvedValueOnce({ data: mockData });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText('AWS')).toBeInTheDocument();
      expect(screen.getByText('Azure')).toBeInTheDocument();
    });

    const filterSelect = screen.getByRole('combobox');
    fireEvent.change(filterSelect, { target: { value: 'team1' } });

    expect(screen.getByText('AWS')).toBeInTheDocument();
    expect(screen.queryByText('Azure')).not.toBeInTheDocument();
  });
});