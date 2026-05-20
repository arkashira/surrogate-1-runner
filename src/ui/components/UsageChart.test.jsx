import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import UsageChart from './UsageChart';

const mockData = [
  { date: '2023-01-01', tokens: 1000, cost: 0.1, model: 'model1', endpoint: 'endpoint1' },
  { date: '2023-01-02', tokens: 1500, cost: 0.15, model: 'model1', endpoint: 'endpoint1' },
  { date: '2023-01-01', tokens: 2000, cost: 0.2, model: 'model2', endpoint: 'endpoint2' },
];

describe('UsageChart', () => {
  it('renders the chart with all data initially', () => {
    render(<UsageChart data={mockData} />);
    expect(screen.getByText('Tokens')).toBeInTheDocument();
    expect(screen.getByText('Cost')).toBeInTheDocument();
  });

  it('filters data by model', () => {
    render(<UsageChart data={mockData} />);
    const modelSelect = screen.getByRole('combobox', { name: /model/i });
    fireEvent.change(modelSelect, { target: { value: 'model1' } });
    expect(screen.getByText('model1')).toBeInTheDocument();
    expect(screen.queryByText('model2')).not.toBeInTheDocument();
  });

  it('filters data by endpoint', () => {
    render(<UsageChart data={mockData} />);
    const endpointSelect = screen.getByRole('combobox', { name: /endpoint/i });
    fireEvent.change(endpointSelect, { target: { value: 'endpoint1' } });
    expect(screen.getByText('endpoint1')).toBeInTheDocument();
    expect(screen.queryByText('endpoint2')).not.toBeInTheDocument();
  });
});