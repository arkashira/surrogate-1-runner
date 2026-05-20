import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import ModelList from './ModelList';

const mockModels = [
  {
    name: 'ModelA',
    version: '1.0',
    complianceStatus: 'Pass',
    lastAuditTimestamp: '2023-05-01T12:00:00Z'
  },
  {
    name: 'ModelB',
    version: '2.0',
    complianceStatus: 'Fail',
    lastAuditTimestamp: '2023-05-02T12:00:00Z'
  }
];

describe('ModelList Component', () => {
  it('renders a list of models with their details', () => {
    render(<ModelList models={mockModels} />);
    
    expect(screen.getByText('ModelA')).toBeInTheDocument();
    expect(screen.getByText('1.0')).toBeInTheDocument();
    expect(screen.getByText('Pass')).toBeInTheDocument();
    expect(screen.getByText('2023-05-01T12:00:00Z')).toBeInTheDocument();

    expect(screen.getByText('ModelB')).toBeInTheDocument();
    expect(screen.getByText('2.0')).toBeInTheDocument();
    expect(screen.getByText('Fail')).toBeInTheDocument();
    expect(screen.getByText('2023-05-02T12:00:00Z')).toBeInTheDocument();
  });

  it('filters models by status', () => {
    render(<ModelList models={mockModels} />);
    
    const filterInput = screen.getByPlaceholderText('Filter by status');
    fireEvent.change(filterInput, { target: { value: 'Pass' } });
    
    expect(screen.getByText('ModelA')).toBeInTheDocument();
    expect(screen.queryByText('ModelB')).not.toBeInTheDocument();
  });

  it('filters models by name', () => {
    render(<ModelList models={mockModels} />);
    
    const filterInput = screen.getByPlaceholderText('Filter by name');
    fireEvent.change(filterInput, { target: { value: 'ModelA' } });
    
    expect(screen.getByText('ModelA')).toBeInTheDocument();
    expect(screen.queryByText('ModelB')).not.toBeInTheDocument();
  });
});