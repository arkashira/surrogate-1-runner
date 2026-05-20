import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ComponentComparison from '../ComponentComparison';

test('filters components by CPU, GPU, and RAM', () => {
  const components = [
    { id: 1, name: 'Component 1', cpu: 'Intel i7', gpu: 'NVIDIA GTX', ram: '16GB' },
    { id: 2, name: 'Component 2', cpu: 'AMD Ryzen', gpu: 'AMD Radeon', ram: '8GB' },
  ];

  render(<ComponentComparison components={components} />);

  // Filter by CPU
  fireEvent.change(screen.getByLabelText(/CPU:/i), { target: { value: 'Intel' } });
  expect(screen.getByText(/Component 1/i)).toBeInTheDocument();
  expect(screen.queryByText(/Component 2/i)).not.toBeInTheDocument();

  // Filter by GPU
  fireEvent.change(screen.getByLabelText(/GPU:/i), { target: { value: 'Radeon' } });
  expect(screen.getByText(/Component 2/i)).toBeInTheDocument();
  expect(screen.queryByText(/Component 1/i)).not.toBeInTheDocument();

  // Filter by RAM
  fireEvent.change(screen.getByLabelText(/RAM:/i), { target: { value: '16GB' } });
  expect(screen.getByText(/Component 1/i)).toBeInTheDocument();
  expect(screen.queryByText(/Component 2/i)).not.toBeInTheDocument();
});