import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import AnalyticsDashboard from './AnalyticsDashboard';
import { fetchOnboardingCompletionData } from '../services/api';

jest.mock('../services/api');

describe('AnalyticsDashboard', () => {
  beforeEach(() => {
    fetchOnboardingCompletionData.mockResolvedValue([
      { step: 'Step 1', completionRate: 80 },
      { step: 'Step 2', completionRate: 65 },
      { step: 'Step 3', completionRate: 75 },
    ]);
  });

  it('renders the dashboard with default time period', async () => {
    render(<AnalyticsDashboard />);
    expect(screen.getByText('Onboarding Completion Rates')).toBeInTheDocument();
    expect(screen.getByLabelText('Select Time Period:')).toBeInTheDocument();
    expect(screen.getByText('Last Week')).toBeInTheDocument();
    expect(await screen.findByText('Step 1')).toBeInTheDocument();
  });

  it('updates data when time period changes', async () => {
    render(<AnalyticsDashboard />);
    fireEvent.change(screen.getByLabelText('Select Time Period:'), { target: { value: 'month' } });
    expect(fetchOnboardingCompletionData).toHaveBeenCalledWith('month');
  });
});