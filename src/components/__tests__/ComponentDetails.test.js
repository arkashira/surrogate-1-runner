import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { fetchComponentDetails } from '../utils/api';
import ComponentDetails from '../ComponentDetails';

jest.mock('../utils/api');

describe('ComponentDetails', () => {
  it('renders component details correctly', async () => {
    const mockData = {
      name: 'Test Component',
      description: 'This is a test component.',
      performanceBenchmarks: ['Benchmark 1', 'Benchmark 2'],
    };

    fetchComponentDetails.mockResolvedValue(mockData);

    render(
      <Router>
        <Routes>
          <Route path="/components/:id" element={<ComponentDetails />} />
        </Routes>
      </Router>,
      { route: '/components/1' }
    );

    expect(screen.getByText('Loading...')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Test Component')).toBeInTheDocument();
      expect(screen.getByText('This is a test component.')).toBeInTheDocument();
      expect(screen.getByText('Benchmark 1')).toBeInTheDocument();
      expect(screen.getByText('Benchmark 2')).toBeInTheDocument();
    });
  });

  it('displays error message when fetching fails', async () => {
    fetchComponentDetails.mockRejectedValue(new Error('Failed to fetch'));

    render(
      <Router>
        <Routes>
          <Route path="/components/:id" element={<ComponentDetails />} />
        </Routes>
      </Router>,
      { route: '/components/1' }
    );

    await waitFor(() => {
      expect(screen.getByText('Error: Failed to fetch')).toBeInTheDocument();
    });
  });
});