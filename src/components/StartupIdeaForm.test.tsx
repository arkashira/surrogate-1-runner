import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import StartupIdeaForm from './StartupIdeaForm';

describe('StartupIdeaForm', () => {
  it('renders the form with all fields', () => {
    render(<StartupIdeaForm />);

    expect(screen.getByLabelText('Problem Statement')).toBeInTheDocument();
    expect(screen.getByLabelText('Solution Statement')).toBeInTheDocument();
    expect(screen.getByLabelText('Total Addressable Market (TAM)')).toBeInTheDocument();
    expect(screen.getByLabelText('Serviceable Available Market (SAM)')).toBeInTheDocument();
    expect(screen.getByLabelText('Serviceable Obtainable Market (SOM)')).toBeInTheDocument();
    expect(screen.getByLabelText('Unit Economics')).toBeInTheDocument();
    expect(screen.getByLabelText('Competitive Analysis')).toBeInTheDocument();
    expect(screen.getByText('Submit')).toBeInTheDocument();
  });

  it('shows validation errors when submitting an empty form', async () => {
    render(<StartupIdeaForm />);

    fireEvent.click(screen.getByText('Submit'));

    expect(await screen.findByText('Problem statement is required')).toBeInTheDocument();
    expect(screen.getByText('Solution statement is required')).toBeInTheDocument();
    expect(screen.getByText('Total Addressable Market is required')).toBeInTheDocument();
    expect(screen.getByText('Serviceable Available Market is required')).toBeInTheDocument();
    expect(screen.getByText('Serviceable Obtainable Market is required')).toBeInTheDocument();
    expect(screen.getByText('Unit economics is required')).toBeInTheDocument();
    expect(screen.getByText('Competitive analysis is required')).toBeInTheDocument();
  });
});