import React from 'react';
import { render } from '@testing-library/react';
import ComparisonTable from '../ComparisonTable';

test('renders comparison table with variants', () => {
  const variants = [
    {
      name: 'Variant 1',
      openaiCompatibility: true,
      containerizationSupport: false,
      integrationPatterns: ['Pattern A', 'Pattern B']
    },
    {
      name: 'Variant 2',
      openaiCompatibility: false,
      containerizationSupport: true,
      integrationPatterns: ['Pattern C']
    }
  ];

  const { getByText } = render(<ComparisonTable variants={variants} />);

  expect(getByText('Variant 1')).toBeInTheDocument();
  expect(getByText('Yes')).toBeInTheDocument();
  expect(getByText('No')).toBeInTheDocument();
  expect(getByText('Pattern A, Pattern B')).toBeInTheDocument();

  expect(getByText('Variant 2')).toBeInTheDocument();
  expect(getByText('No')).toBeInTheDocument();
  expect(getByText('Yes')).toBeInTheDocument();
  expect(getByText('Pattern C')).toBeInTheDocument();
});