import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import App from './App';

describe('App', () => {
  it('renders the WorkflowDashboard component', () => {
    render(<App />);
    expect(screen.getByText('Workflow Management Dashboard')).toBeInTheDocument();
  });

  it('adds a new tool when the add tool button is clicked', () => {
    render(<App />);
    fireEvent.change(screen.getByPlaceholderText('Tool Name'), { target: { value: 'New Tool' } });
    fireEvent.click(screen.getByText('Add Tool'));
    expect(screen.getByText('New Tool')).toBeInTheDocument();
  });

  it('removes a tool when the remove button is clicked', () => {
    render(<App />);
    fireEvent.change(screen.getByPlaceholderText('Tool Name'), { target: { value: 'New Tool' } });
    fireEvent.click(screen.getByText('Add Tool'));
    fireEvent.click(screen.getByText('Remove'));
    expect(screen.queryByText('New Tool')).not.toBeInTheDocument();
  });

  it('updates a tool status when the toggle status button is clicked', () => {
    render(<App />);
    fireEvent.change(screen.getByPlaceholderText('Tool Name'), { target: { value: 'New Tool' } });
    fireEvent.click(screen.getByText('Add Tool'));
    fireEvent.click(screen.getByText('Toggle Status'));
    expect(screen.getByText('inactive')).toBeInTheDocument();
  });
});