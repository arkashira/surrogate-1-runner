import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TimeRangeSelector from './TimeRangeSelector';

describe('TimeRangeSelector', () => {
  it('renders without crashing', () => {
    render(<TimeRangeSelector onRangeChange={() => {}} />);
    expect(screen.getByLabelText('Select Time Range:')).toBeInTheDocument();
  });

  it('calls onRangeChange when a new option is selected', () => {
    const mockOnRangeChange = jest.fn();
    render(<TimeRangeSelector onRangeChange={mockOnRangeChange} />);
    fireEvent.change(screen.getByLabelText('Select Time Range:'), { target: { value: '3' } });
    expect(mockOnRangeChange).toHaveBeenCalledWith('3');
  });
});