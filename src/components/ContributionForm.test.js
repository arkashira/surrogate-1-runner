import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ContributionForm from './ContributionForm';

test('validates contribution amount boundaries', () => {
  render(<ContributionForm />);
  
  const amountInput = screen.getByLabelText(/Contribution Amount $/i);
  const submitButton = screen.getByText('Save Contribution Settings');
  
  // Test too low
  fireEvent.change(amountInput, { target: { value: '0' } });
  fireEvent.click(submitButton);
  expect(screen.getByText(/must be between $1 and $10,000/i)).toBeInTheDocument();
  
  // Test too high
  fireEvent.change(amountInput, { target: { value: '10001' } });
  fireEvent.click(submitButton);
  expect(screen.getByText(/must be between $1 and $10,000/i)).toBeInTheDocument();
  
  // Test valid
  fireEvent.change(amountInput, { target: { value: '50' } });
  fireEvent.click(submitButton);
  expect(screen.queryByText(/error/i)).not.toBeInTheDocument();
});

test('formats contribution date correctly', () => {
  render(<ContributionForm />);
  const dateSelect = screen.getByLabelText(/Monthly Contribution Date/i);
  fireEvent.change(dateSelect, { target: { value: '07' } });
  expect(dateSelect.value).toBe('07');
});