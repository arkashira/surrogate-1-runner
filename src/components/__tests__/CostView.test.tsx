import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import CostView from '../CostView';

describe('CostView', () => {
  it('renders correctly', () => {
    const { getByText } = render(<CostView />);
    expect(getByText('Unified Cost View')).toBeInTheDocument();
  });

  it('displays the selected provider', () => {
    const { getByText, getByLabelText } = render(<CostView />);

    fireEvent.change(getByLabelText('Cloud Provider'), { target: { value: 'aws' } });
    expect(getByText('Showing costs for AWS')).toBeInTheDocument();
  });
});