import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import PLTrend from './PLTrend';

describe('PLTrend', () => {
  it('renders without crashing', () => {
    render(<PLTrend />);
    expect(screen.getByLabelText('Select Time Range:')).toBeInTheDocument();
  });

  it('updates the chart when the time range changes', () => {
    render(<PLTrend />);
    fireEvent.change(screen.getByLabelText('Select Time Range:'), { target: { value: '6' } });
    // Add assertions to check if the chart updates
  });
});