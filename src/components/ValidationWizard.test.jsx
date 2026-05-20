import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import ValidationWizard from './ValidationWizard';

test('renders wizard steps and allows navigation', () => {
  const { getByText, getByRole } = render(<ValidationWizard />);
  
  // Check initial step
  expect(getByText(/Hypothesis/i)).toBeInTheDocument();
  
  // Fill in the hypothesis
  fireEvent.change(getByRole('textbox'), { target: { value: 'Test Hypothesis' } });
  
  // Navigate to next step
  fireEvent.click(getByText(/Next/i));
  expect(getByText(/Metrics/i)).toBeInTheDocument();
  
  // Navigate back
  fireEvent.click(getByText(/Back/i));
  expect(getByText(/Hypothesis/i)).toBeInTheDocument();
  
  // Save progress
  fireEvent.click(getByText(/Save Progress/i));
  
  // Finish the wizard
  fireEvent.click(getByText(/Next/i));
  fireEvent.click(getByText(/Finish/i));
  
  // Check summary
  expect(getByText(/Summary/i)).toBeInTheDocument();
});