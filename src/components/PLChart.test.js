import React from 'react';
import { render, screen } from '@testing-library/react';
import PLChart from './PLChart';

describe('PLChart', () => {
  const mockData = [
    { date: '2023-01-01', value: 1000 },
    { date: '2023-02-01', value: 2000 },
    { date: '2023-03-01', value: 1500 },
  ];

  it('renders without crashing', () => {
    render(<PLChart data={mockData} />);
    expect(screen.getByRole('img')).toBeInTheDocument();
  });
});