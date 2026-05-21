import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import WorkflowDashboard from './WorkflowDashboard';
import { Tool } from '../types';

describe('WorkflowDashboard', () => {
  const mockTools: Tool[] = [
    { id: '1', name: 'Tool 1', status: 'active' },
    { id: '2', name: 'Tool 2', status: 'inactive' },
  ];

  const mockOnAddTool = jest.fn();
  const mockOnRemoveTool = jest.fn();
  const mockOnUpdateTool = jest.fn();

  beforeEach(() => {
    render(
      <WorkflowDashboard
        tools={mockTools}
        onAddTool={mockOnAddTool}
        onRemoveTool={mockOnRemoveTool}
        onUpdateTool={mockOnUpdateTool}
      />
    );
  });

  it('renders the dashboard title', () => {
    expect(screen.getByText('Workflow Management Dashboard')).toBeInTheDocument();
  });

  it('displays the list of tools', () => {
    expect(screen.getByText('Tool 1')).toBeInTheDocument();
    expect(screen.getByText('Tool 2')).toBeInTheDocument();
  });

  it('calls onRemoveTool when the remove button is clicked', () => {
    fireEvent.click(screen.getAllByText('Remove')[0]);
    expect(mockOnRemoveTool).toHaveBeenCalledWith('1');
  });

  it('calls onUpdateTool when the toggle status button is clicked', () => {
    fireEvent.click(screen.getAllByText('Toggle Status')[0]);
    expect(mockOnUpdateTool).toHaveBeenCalledWith({ id: '1', name: 'Tool 1', status: 'inactive' });
  });

  it('calls onAddTool when the add tool button is clicked', () => {
    fireEvent.change(screen.getByPlaceholderText('Tool Name'), { target: { value: 'New Tool' } });
    fireEvent.click(screen.getByText('Add Tool'));
    expect(mockOnAddTool).toHaveBeenCalledWith({ id: '', name: 'New Tool', status: 'inactive' });
  });
});