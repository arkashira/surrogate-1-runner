import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import BuildComparison from '../BuildComparison';

test('renders build comparison component', () => {
  const buildOptions = [
    { name: 'Option 1', price: 100, performance: 80 },
    { name: 'Option 2', price: 150, performance: 90 },
    // Add more build options as needed
  ];

  render(<BuildComparison buildOptions={buildOptions} />);

  expect(screen.getByText('Build Comparison')).toBeInTheDocument();
  expect(screen.getByText('Price')).toBeInTheDocument();
  expect(screen.getByText('Performance')).toBeInTheDocument();

  fireEvent.change(screen.getByRole('combobox'), { target: { value: 'performance' } });
  expect(screen.getByText('Option 2')).toBeInTheDocument();
  expect(screen.getByText('Option 1')).toBeInTheDocument();
});