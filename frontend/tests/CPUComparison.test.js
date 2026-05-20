import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import CPUComparison from '../components/CPUComparison';

test('renders CPU comparison page', () => {
  render(<CPUComparison />);
  expect(screen.getByText(/CPU Comparison/i)).toBeInTheDocument();
});

test('filters CPUs by brand', () => {
  render(<CPUComparison />);
  fireEvent.change(screen.getByLabelText(/Brand:/i), { target: { value: 'Intel' } });
  // Assuming there is at least one Intel CPU in the list
  expect(screen.getByText(/Intel/i)).toBeInTheDocument();
});

test('filters CPUs by price', () => {
  render(<CPUComparison />);
  fireEvent.change(screen.getByLabelText(/Max Price:/i), { target: { value: '500' } });
  // Assuming there is at least one CPU priced under $500 in the list
  expect(screen.getByText(/Price/i)).toBeInTheDocument();
});

test('filters CPUs by performance', () => {
  render(<CPUComparison />);
  fireEvent.change(screen.getByLabelText(/Min Performance:/i), { target: { value: '4.0' } });
  // Assuming there is at least one CPU with performance >= 4.0 in the list
  expect(screen.getByText(/Performance/i)).toBeInTheDocument();
});