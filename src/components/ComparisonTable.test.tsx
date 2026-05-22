import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ComparisonTable from './ComparisonTable';
import { ClawVariant } from '../types';

const mockVariants: ClawVariant[] = [
  {
    id: '1',
    name: 'Variant A',
    capabilities: {
      'Feature X': true,
      'Feature Y': false,
      'Feature Z': true,
    },
  },
  {
    id: '2',
    name: 'Variant B',
    capabilities: {
      'Feature X': false,
      'Feature Y': true,
      'Feature Z': true,
    },
  },
];

describe('ComparisonTable', () => {
  it('renders the comparison table with selected variants', () => {
    render(<ComparisonTable variants={mockVariants} />);

    // Check if variant selection checkboxes are rendered
    expect(screen.getByText('Variant A')).toBeInTheDocument();
    expect(screen.getByText('Variant B')).toBeInTheDocument();

    // Select Variant A
    fireEvent.click(screen.getByLabelText('Variant A'));

    // Check if Variant A's capabilities are displayed
    expect(screen.getByText('Feature X')).toBeInTheDocument();
    expect(screen.getByText('✓')).toBeInTheDocument();
    expect(screen.getByText('✗')).toBeInTheDocument();
    expect(screen.getByText('✓')).toBeInTheDocument();

    // Select Variant B
    fireEvent.click(screen.getByLabelText('Variant B'));

    // Check if Variant B's capabilities are displayed
    expect(screen.getByText('✗')).toBeInTheDocument();
    expect(screen.getByText('✓')).toBeInTheDocument();
    expect(screen.getByText('✓')).toBeInTheDocument();
  });
});