import React from 'react';
import { render } from '@testing-library/react';
import TroubleshootingGuide from '../TroubleshootingGuide';

describe('TroubleshootingGuide', () => {
  it('renders without crashing', () => {
    render(<TroubleshootingGuide />);
  });

  it('displays the correct title', () => {
    const { getByText } = render(<TroubleshootingGuide />);
    expect(getByText('CFD Simulation Troubleshooting Guide')).toBeInTheDocument();
  });

  it('displays common issues and steps', () => {
    const { getByText } = render(<TroubleshootingGuide />);
    expect(getByText('Mesh Quality Issues')).toBeInTheDocument();
    expect(getByText('Check the mesh quality metrics (e.g., skewness, aspect ratio).')).toBeInTheDocument();
    expect(getByText('Boundary Conditions')).toBeInTheDocument();
    expect(getByText('Verify the boundary conditions are correctly applied.')).toBeInTheDocument();
    expect(getByText('Numerical Instability')).toBeInTheDocument();
    expect(getByText('Reduce the time step size.')).toBeInTheDocument();
    expect(getByText('Convergence Issues')).toBeInTheDocument();
    expect(getByText('Check the residual history to identify where convergence is stalling.')).toBeInTheDocument();
  });
});