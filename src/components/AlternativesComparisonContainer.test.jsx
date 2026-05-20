import React from 'react';
import { render } from '@testing-library/react';
import AlternativesComparisonContainer from './AlternativesComparisonContainer';

describe('AlternativesComparisonContainer', () => {
  it('renders alternatives comparison and list', () => {
    const alternatives = [
      { name: 'Alternative 1', performance: 10, price: 100 },
      { name: 'Alternative 2', performance: 20, price: 200 },
    ];

    const { getByText } = render(<AlternativesComparisonContainer alternatives={alternatives} />);
    expect(getByText('Alternative 1')).toBeInTheDocument();
    expect(getByText('Alternative 2')).toBeInTheDocument();
  });
});