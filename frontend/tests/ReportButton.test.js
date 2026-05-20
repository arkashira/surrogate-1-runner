import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Dashboard from '../src/pages/Dashboard';
import { AuthContext } from '../src/context/AuthContext';
import { BrowserRouter as Router } from 'react-router-dom';
import '@testing-library/jest-dom/extend-expect';

// Mock the toast library (e.g., react-toastify)
jest.mock('react-toastify', () => ({
  toast: {
    error: jest.fn(),
  },
}));

// Mock global fetch
global.fetch = jest.fn();

const mockUser = { id: '123', name: 'Test User' };

const renderDashboard = () => {
  render(
    <AuthContext.Provider value={{ user: mockUser, isAuthenticated: true }}>
      <Router>
        <Dashboard />
      </Router>
    </AuthContext.Provider>
  );
};

describe('Generate Investor Report button', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders button and shows spinner on click', async () => {
    // Mock successful PDF generation
    const blob = new Blob(['PDF content'], { type: 'application/pdf' });
    global.fetch.mockResolvedValueOnce({
      ok: true,
      blob: async () => blob,
    });

    renderDashboard();

    const button = screen.getByRole('button', { name: /generate investor report/i });
    expect(button).toBeInTheDocument();

    // Click the button
    fireEvent.click(button);

    // Spinner should appear
    const spinner = screen.getByTestId('report-spinner');
    expect(spinner).toBeInTheDocument();

    // Wait for fetch to resolve and spinner to disappear
    await waitFor(() => expect(spinner).not.toBeInTheDocument());

    // Ensure fetch was called with correct endpoint
    expect(fetch).toHaveBeenCalledWith('/api/generate-report', expect.any(Object));
  });

  test('shows toast error when generation fails', async () => {
    // Mock failed PDF generation
    global.fetch.mockResolvedValueOnce({
      ok: false,
      statusText: 'Internal Server Error',
    });

    renderDashboard();

    const button = screen.getByRole('button', { name: /generate investor report/i });
    fireEvent.click(button);

    // Spinner should appear
    const spinner = screen.getByTestId('report-spinner');
    expect(spinner).toBeInTheDocument();

    // Wait for error handling
    await waitFor(() => expect(spinner).not.toBeInTheDocument());

    // Toast error should be called
    const { toast } = require('react-toastify');
    expect(toast.error).toHaveBeenCalledWith(
      'Failed to generate investor report. Please try again.'
    );
  });

  test('button is responsive on tablet view', () => {
    // Set viewport to tablet width
    global.innerWidth = 768;
    global.dispatchEvent(new Event('resize'));

    renderDashboard();

    const button = screen.getByRole('button', { name: /generate investor report/i });
    expect(button).toBeInTheDocument();

    // Ensure button has responsive class (example: 'btn-tablet')
    expect(button).toHaveClass('btn-tablet');
  });
});