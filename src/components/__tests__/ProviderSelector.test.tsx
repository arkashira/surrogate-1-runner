import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import ProviderSelector from '../ProviderSelector';

describe('ProviderSelector', () => {
  it('renders correctly', () => {
    const { getByLabelText } = render(<ProviderSelector onProviderChange={() => {}} />);
    expect(getByLabelText('Cloud Provider')).toBeInTheDocument();
  });

  it('calls onProviderChange when a provider is selected', () => {
    const mockOnProviderChange = jest.fn();
    const { getByLabelText } = render(<ProviderSelector onProviderChange={mockOnProviderChange} />);

    fireEvent.change(getByLabelText('Cloud Provider'), { target: { value: 'aws' } });
    expect(mockOnProviderChange).toHaveBeenCalledWith('aws');
  });
});