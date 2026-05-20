import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import BuildWizard from '../components/BuildWizard';

describe('BuildWizard', () => {
  it('displays steps and validates compatibility', () => {
    const { getByText, queryByText } = render(<BuildWizard />);

    // Select CPU
    fireEvent.click(getByText('CPU'));
    fireEvent.click(getByText('Intel Core i9-13900K'));

    // Validate GPU compatibility
    fireEvent.click(getByText('GPU'));
    fireEvent.click(getByText('NVIDIA GeForce RTX 4090'));
    expect(queryByText('Incompatible')).toBeNull();

    // ... continue for other components
  });

  it('displays summary with total price and performance estimate', () => {
    const { getByText } = render(<BuildWizard />);

    // Complete all steps
    // ...

    fireEvent.click(getByText('Summary'));

    expect(getByText('Total Price: $3000')).toBeInTheDocument();
    expect(getByText('Performance Estimate: High')).toBeInTheDocument();
  });
});