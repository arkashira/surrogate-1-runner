import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import CostMetrics from './CostMetrics';

describe('CostMetrics component', () => {
  it('renders cost data', async () => {
    const costService = {
      getCostData: jest.fn(() => Promise.resolve({ costData: [{ cost: 100 }] })),
    };
    const { getByText } = render(<CostMetrics costService={costService} />);
    await waitFor(() => getByText('Cost Metrics'));
    expect(getByText('100')).toBeInTheDocument();
  });
});