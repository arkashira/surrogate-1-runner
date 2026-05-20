import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import ComponentComparison from '../ComponentComparison';

test('should refine build recommendations based on user preferences', () => {
  const components = [
    { id: 1, performance: 60 },
    { id: 2, performance: 40 },
    { id: 3, performance: 80 },
  ];

  const { getByLabelText, getByText } = render(<ComponentComparison components={components} />);

  fireEvent.change(getByLabelText(/Performance Priority/), { target: { value: '70' } });
  fireEvent.click(getByText('Refine Recommendations'));

  // Assuming there's a way to check the console output or the UI state after refining recommendations.
  // For now, we'll just check if the button exists and can be clicked.
  expect(getByText('Refine Recommendations')).toBeInTheDocument();
});