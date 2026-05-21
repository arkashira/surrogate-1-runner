  import React from 'react';
  import { render, screen } from '@testing-library/react';
  import TroubleshootingGuide from './TroubleshootingGuide';

  describe('TroubleshootingGuide', () => {
    it('renders the troubleshooting guide', () => {
      render(<TroubleshootingGuide />);
      expect(screen.getByText('CFD Simulation Troubleshooting Guide')).toBeInTheDocument();
    });

    it('displays common errors and solutions', () => {
      render(<TroubleshootingGuide />);
      expect(screen.getByText('Error: Convergence Failure')).toBeInTheDocument();
      expect(screen.getByText('Error: Mesh Quality Issues')).toBeInTheDocument();
      expect(screen.getByText('Error: Boundary Condition Errors')).toBeInTheDocument();
      expect(screen.getByText('Error: Numerical Instability')).toBeInTheDocument();
    });
  });